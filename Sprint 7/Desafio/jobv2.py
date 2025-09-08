import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from pyspark.sql import Window
from pyspark.sql.types import IntegerType

# ------------------------------
# Inicialização do Job
# ------------------------------
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ------------------------------
# Caminhos
# ------------------------------
TRUSTED_CSV = "s3://data-lake-isa1/Trusted/Movies/CSV/"
TRUSTED_JSON = "s3://data-lake-isa1/Trusted/Movies/JSON/"
REFINED_PATH = "s3://data-lake-isa1/Refined/"

# ------------------------------
# Funções auxiliares
# ------------------------------
def read_trusted_parquet(paths):
    dfs = []
    for path in paths:
        try:
            df = spark.read.parquet(path)
            if df.count() > 0:
                for c in ["ano", "mes", "dia"]:
                    if c not in df.columns:
                        df = df.withColumn(c, F.lit(None).cast("int"))
                if "processed_date" not in df.columns:
                    df = df.withColumn("processed_date", F.lit(None).cast("string"))
                dfs.append(df)
        except Exception as e:
            print(f"Erro ao ler {path}: {str(e)}")
    
    if not dfs:
        raise Exception("Nenhum dado encontrado!")
    
    # Union dos DataFrames com padronização de colunas
    all_cols = sorted(set().union(*[df.columns for df in dfs]))
    standardized = []
    for df in dfs:
        for c in all_cols:
            if c not in df.columns:
                df = df.withColumn(c, F.lit(None))
        standardized.append(df.select(*all_cols))
    
    result = standardized[0]
    for df in standardized[1:]:
        result = result.unionByName(df, allowMissingColumns=True)
    return result

def normalize_columns(df):
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
        .withColumnRenamed("numerovotos", "numero_votos"))

def deduplicate_movies(df):
    window_spec = Window.partitionBy("id").orderBy(F.desc("processed_date"))
    return df.withColumn("row_number", F.row_number().over(window_spec)) \
             .filter("row_number = 1").drop("row_number")

def generate_hash_key(*cols):
    return F.abs(F.hash(F.concat_ws("_", *cols))).cast(IntegerType())

def create_dim_time():
    """Criar dimensão tempo completa com diferentes granularidades"""
    time_data = []
    for year in range(1900, 2030):
        for month in range(1, 13):
            for day in range(1, 32):
                # Validação básica de dias por mês
                if month in [4, 6, 9, 11] and day > 30:
                    continue
                if month == 2 and day > 29:
                    continue
                
                # Calcular granularidades temporais
                decade = (year // 10) * 10
                century = (year // 100) * 100 + 1
                quarter = ((month - 1) // 3) + 1
                
                # Nome do mês
                month_names = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                              "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
                month_name = month_names[month]
                
                # Trimestre nome
                quarter_names = ["", "Q1", "Q2", "Q3", "Q4"]
                quarter_name = quarter_names[quarter]
                
                time_data.append((
                    year, month, day, decade, century, quarter, 
                    month_name, quarter_name, f"{year}-{month:02d}-{day:02d}"
                ))
    
    time_df = spark.createDataFrame(time_data, [
        "ano", "mes", "dia", "decada", "seculo", "trimestre",
        "nome_mes", "nome_trimestre", "data_completa"
    ])
    
    return time_df.withColumn("time_key", generate_hash_key("ano", "mes", "dia"))

def save_table(df, name, partition_keys=[]):
    path = f"{REFINED_PATH}{name}/"
    if partition_keys:
        df.write.mode("overwrite").partitionBy(*partition_keys).parquet(path)
    else:
        df.write.mode("overwrite").parquet(path)

# ------------------------------
# PROCESSAMENTO PRINCIPAL
# ------------------------------
movies_df = read_trusted_parquet([TRUSTED_CSV, TRUSTED_JSON])
movies_df = normalize_columns(movies_df)

# ------------------------------
# Etapa de filtragem e desduplicação
# ------------------------------
initial_count = movies_df.count()
movies_df = movies_df.filter(F.col("id").isNotNull() & F.col("titulo_principal").isNotNull())
rows_dropped = initial_count - movies_df.count()
print(f"🧹 Registros removidos devido a ID ou título nulo: {rows_dropped}")

movies_df = deduplicate_movies(movies_df)

# Adicionar origin_country_str
if "origin_country" in movies_df.columns:
    movies_df = movies_df.withColumn("origin_country_str",
        F.when(F.col("origin_country").isNotNull() & (F.size(F.col("origin_country")) > 0),
               F.col("origin_country")[0]).otherwise(F.lit("Unknown")))
else:
    movies_df = movies_df.withColumn("origin_country_str", F.lit("Unknown"))

# ------------------------------
# Processar production_companies CORRETAMENTE
# ------------------------------
if "production_companies" in movies_df.columns:
    # Explodir o array de companies para ter uma linha por filme-company
    movies_companies = movies_df.select(
        F.col("id").alias("movie_id"),
        F.explode_outer("production_companies").alias("company")
    ).select(
        "movie_id",
        F.col("company.id").alias("company_id"),
        F.col("company.name").alias("company_name"),
        F.col("company.logo_path").alias("company_logo"),
        F.col("company.origin_country").alias("company_country")
    ).filter(F.col("company_id").isNotNull())
    
    # Criar dimensão companies
    dim_companies = movies_companies.select(
        "company_id", "company_name", "company_logo", "company_country"
    ).dropDuplicates().withColumn("company_key", generate_hash_key("company_id"))
    
    # Mapear movie para company_key (pegar apenas a primeira company por filme para simplificar)
    movie_company_mapping = movies_companies.join(
        dim_companies.select("company_id", "company_key"),
        on="company_id"
    ).select("movie_id", "company_key") \
    .withColumn("rn", F.row_number().over(Window.partitionBy("movie_id").orderBy("company_key"))) \
    .filter("rn = 1").drop("rn")
    
else:
    # Se não existir production_companies, criar dimensão vazia
    dim_companies = spark.createDataFrame([], ["company_id", "company_name", "company_logo", "company_country", "company_key"])
    movie_company_mapping = spark.createDataFrame([], ["movie_id", "company_key"])

# ------------------------------
# Criar dimensões
# ------------------------------

# Dimensão Tempo
dim_time = create_dim_time()

# Dimensão Artistas
dim_artists = movies_df.select(
    "nome_artista", "personagem", "profissao", "genero_artista",
    "ano_nascimento", "ano_falecimento", "titulos_mais_conhecidos"
).filter(F.col("nome_artista").isNotNull()).distinct() \
 .withColumn("artist_key", generate_hash_key("nome_artista", "personagem"))

# Dimensão Filmes (informações textuais)
dim_movies = movies_df.select(
    F.col("id").alias("movie_id"),
    "titulo_principal",
    "titulo_original", 
    "genero",
    "origin_country_str"
).dropDuplicates(["movie_id"]) \
 .withColumn("movie_key", generate_hash_key("movie_id"))

# ------------------------------
# Criar tabela FATO - APENAS VALORES NUMÉRICOS
# ------------------------------

# Primeiro, criar o mapeamento time_key baseado no ano_lancamento
movies_with_time = movies_df.withColumn("ano_ref", F.coalesce(F.col("ano_lancamento"), F.lit(1900))) \
    .withColumn("mes_ref", F.lit(1)) \
    .withColumn("dia_ref", F.lit(1)) \
    .withColumn("time_key", generate_hash_key("ano_ref", "mes_ref", "dia_ref"))

# Criar artist_key 
movies_with_keys = movies_with_time.withColumn("artist_key", 
    F.when(F.col("nome_artista").isNotNull(), 
           generate_hash_key("nome_artista", "personagem"))
     .otherwise(F.lit(-1).cast(IntegerType())))

# Adicionar movie_key
movies_with_keys = movies_with_keys.withColumn("movie_key", generate_hash_key("id"))

# Juntar com company_key
movies_final = movies_with_keys.join(
    movie_company_mapping,
    on=movies_with_keys.id == movie_company_mapping.movie_id,
    how="left"
).withColumn("company_key", F.coalesce(F.col("company_key"), F.lit(-1).cast(IntegerType())))

# TABELA FATO - SOMENTE CAMPOS NUMÉRICOS
fact_avaliacoes_filmes = movies_final.select(
    # Chaves das dimensões (numéricas)
    "movie_key",
    "time_key", 
    "artist_key",
    "company_key",
    
    # Métricas numéricas
    F.col("ano_lancamento").cast(IntegerType()).alias("ano_lancamento"),
    F.col("tempo_minutos").cast(IntegerType()).alias("duracao_minutos"),
    F.col("nota_media").cast("double").alias("nota_media"),
    F.col("numero_votos").cast(IntegerType()).alias("numero_votos"),
    
    # Campos de particionamento
    F.coalesce(F.col("ano"), F.lit(2024)).cast(IntegerType()).alias("ano_partition"),
    F.coalesce(F.col("mes"), F.lit(1)).cast(IntegerType()).alias("mes_partition"), 
    F.coalesce(F.col("dia"), F.lit(1)).cast(IntegerType()).alias("dia_partition")
).filter(F.col("movie_key").isNotNull())

# ------------------------------
# Salvar tabelas
# ------------------------------
print("Salvando dimensões...")
save_table(dim_time, "dim_time")
save_table(dim_artists, "dim_artists") 
save_table(dim_companies, "dim_companies")
save_table(dim_movies, "dim_movies")

print("Salvando tabela fato...")
save_table(fact_avaliacoes_filmes, "fact_avaliacoes_filmes", ["ano_partition", "mes_partition", "dia_partition"])

# Estatísticas finais
print("=" * 50)
print("📊 ESTATÍSTICAS FINAIS")
print("=" * 50)

fato_count = fact_avaliacoes_filmes.count()
movies_count = dim_movies.count()
artists_count = dim_artists.count()
companies_count = dim_companies.count()

print(f"📊 Registros na tabela fato: {fato_count}")
print(f"📊 Filmes únicos: {movies_count}")
print(f"📊 Artistas únicos: {artists_count}")
print(f"📊 Companies únicas: {companies_count}")

# Debug adicional para companies
if companies_count > 0:
    print("\n🏢 SAMPLE DE COMPANIES:")
    dim_companies.show(5, truncate=False)
    
    # Verificar quantos filmes têm company_key válida na fato
    filmes_com_company = fact_avaliacoes_filmes.filter(F.col("company_key") != -1).count()
    print(f"📊 Filmes na fato com company válida: {filmes_com_company}")
else:
    print("\n⚠️ ATENÇÃO: Nenhuma company foi processada!")
    
    # Debug: vamos ver como estão os dados originais
    print("🔍 Verificando dados originais de production_companies...")
    if "production_companies" in movies_df.columns:
        sample_companies = movies_df.select("id", "titulo_principal", "production_companies") \
                                   .filter(F.col("production_companies").isNotNull()) \
                                   .limit(3)
        print("Sample de filmes com production_companies:")
        sample_companies.show(truncate=False)
    else:
        print("❌ Campo production_companies não existe no DataFrame!")

job.commit()