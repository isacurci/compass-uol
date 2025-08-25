import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from pyspark.sql import Window

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# --- Caminhos do S3 ---
TRUSTED_CSV = "s3://data-lake-isa1/Trusted/Movies/CSV/"
TRUSTED_JSON = "s3://data-lake-isa1/Trusted/Movies/JSON/"
REFINED_PATH = "s3://data-lake-isa1/Refined/"

# --- Ler Parquet 'CSV' e 'JSON' da Trusted ---
def read_trusted_parquet(paths):
    dfs = []
    for path in paths:
        try:
            df = spark.read.parquet(path)
            if df.count() > 0:
                # Garantir colunas de partição para a união
                for c in ["ano", "mes", "dia"]:
                    if c not in df.columns:
                        df = df.withColumn(c, F.lit(None).cast("int"))
                if "processed_date" not in df.columns:
                    df = df.withColumn("processed_date", F.lit(None).cast("string"))
                dfs.append(df)
                print(f"📂 {path} carregado com {df.count()} registros")
        except Exception as e:
            print(f"⚠️ Erro ao ler {path}: {str(e)}")
    
    if not dfs:
        raise Exception("❌ Nenhum dado encontrado na Trusted!")
    
    # Union inteligente para combinar todos os df
    all_cols = sorted(set().union(*[df.columns for df in dfs]))
    standardized = []
    for df in dfs:
        for c in all_cols:
            if c not in df.columns:
                df = df.withColumn(c, F.lit(None))
        standardized.append(df.select(*all_cols))
    
    # Executa a união dos df
    result = standardized[0]
    for df in standardized[1:]:
        result = result.unionByName(df, allowMissingColumns=True)
        
    print(f"📊 Dataset combinado: {result.count()} registros, {len(result.columns)} colunas")
    return result

# --- Normaliza colunas ---
def normalize_columns(df):
    """Renomeia colunas para um padrão consistente."""
    return (df
        .withColumnRenamed("titulopincipal", "titulo_principal")
        .withColumnRenamed("titulooriginal", "titulo_original")
        .withColumnRenamed("anolancamento", "ano_lancamento")
        .withColumnRenamed("tempominutos", "tempo_minutos")
        .withColumnRenamed("generoartista", "genero_artista")
        .withColumnRenamed("nomeartista", "nome_artista")
        .withColumnRenamed("anonascimento", "ano_nascimento")
        .withColumnRenamed("anofalecimento", "ano_falecimento")
        .withColumnRenamed("titulosmaisconhecidos", "titulos_mais_conhecidos")
        .withColumnRenamed("notamedia", "nota_media")
        .withColumnRenamed("numerovotos", "numero_votos")
    )

# --- Desduplica os registros do filme ---
def deduplicate_movies(df):
    """
    Remove registros duplicados com base no ID do filme, mantendo o mais recente.
    Esta é a parte crucial para resolver o problema de duplicação.
    """
    print(f"🔍 Registros antes da desduplicação: {df.count()}")
    
    # Pegando mais recente

    window_spec = Window.partitionBy("id").orderBy(F.desc("processed_date"))
    
    # Adiciona um número de linha por grupo e filtra para manter apenas o primeiro
    deduped_df = df.withColumn("row_number", F.row_number().over(window_spec)) \
                   .filter("row_number = 1") \
                   .drop("row_number")
                   
    print(f"✅ Registros após desduplicação: {deduped_df.count()}")
    return deduped_df

# --- Criando e salvando as tabelas de dimensão ---
def create_and_save_dimensions(df):

    # DIM_TIME: A chave de tempo será uma combinação das colunas de data
    dim_time = df.select("processed_date","ano_lancamento","ano","mes","dia").distinct()

    # DIM_ARTISTS
    dim_artists = df.select("nome_artista", "personagem", "profissao", "genero_artista",
                            "ano_nascimento", "ano_falecimento", "titulos_mais_conhecidos") \
                    .distinct() \
                    .filter(F.col("nome_artista").isNotNull())

    # Salva as dimensões
    save_refined_table(dim_time, "dim_time", ["ano", "mes", "dia"])
    save_refined_table(dim_artists, "dim_artists")

    return dim_time, dim_artists

# --- Salva uma tabela refinada ---
def save_refined_table(df, name, partition_keys=[]):
    """Função genérica para salvar tabelas."""
    path = f"{REFINED_PATH}{name}/"
    df.write.mode("overwrite").partitionBy(*partition_keys).parquet(path)
    print(f"✅ {name} salvo com {df.count()} registros")

# --- MAIN ---
movies_df = read_trusted_parquet([TRUSTED_CSV, TRUSTED_JSON])
movies_df = normalize_columns(movies_df)

# Nova etapa: Criar a coluna "origin_country_str" logo após a normalização.
if "origin_country" in movies_df.columns:
    movies_df = movies_df.withColumn("origin_country_str",
                       F.when(F.col("origin_country").isNotNull() & (F.size(F.col("origin_country")) > 0),
                               F.col("origin_country")[0])
                         .otherwise(F.lit("Unknown")))
else:
    movies_df = movies_df.withColumn("origin_country_str", F.lit("Unknown"))


# Etapa de filtragem para garantir a integridade dos dados
initial_count = movies_df.count()
movies_df_filtered = movies_df.filter(F.col("id").isNotNull() & F.col("titulo_principal").isNotNull())
rows_dropped = initial_count - movies_df_filtered.count()
print(f"🧹 Registros removidos devido a ID ou título nulo: {rows_dropped}")

# Etapa 1: Remover duplicatas na origem
movies_df_clean = deduplicate_movies(movies_df_filtered)

# Etapa 2: Criar e salvar dimensões. A chave será gerada no join.
dim_time, dim_artists = create_and_save_dimensions(movies_df_clean)

# Etapa 3: Criar a tabela fato e realizar os joins
# Juntando a tabela de filmes limpa com as dimensões para obter as chaves corretas.
fact_movies = movies_df_clean.join(dim_time, on=["processed_date","ano_lancamento","ano","mes","dia"], how="left") \
                             .select(F.col("id").alias("movie_id"),
                                     "titulo_principal", "titulo_original", "ano_lancamento",
                                     "tempo_minutos", "genero", "nota_media", "numero_votos",
                                     F.col("processed_date").alias("time_key"), # Usando processed_date como chave
                                     "origin_country_str", # Usando o país como chave
                                     "ano", "mes", "dia")

# Etapa 4: Salvar a tabela fato
save_refined_table(fact_movies, "fact_movies", ["ano", "mes", "dia"])

job.commit()
