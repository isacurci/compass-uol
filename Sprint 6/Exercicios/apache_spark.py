from pyspark.sql import SparkSession
from pyspark import SparkContext, SQLContext
from pyspark.sql.functions import col, when, rand, floor, lit
from pyspark.sql.types import StringType

# Criando a sessão Spark
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Exercicio Intro") \
    .getOrCreate()

# Etapa 1: Lendo o arquivo como texto simples
df_nomes = spark.read.text("nomes_aleatorios.txt")

# Visualizando os dados
df_nomes.show(5)

# Etapa 2: Ver o schema e renomear coluna para "Nomes"
print("Schema original:")
df_nomes.printSchema()

# Renomeando a coluna 'value' para 'Nomes'
df_nomes = df_nomes.withColumnRenamed("value", "Nomes")

print("\nApós renomear:")
df_nomes.printSchema()
df_nomes.show(10)

# Etapa 3: Adicionar coluna "Escolaridade" com valores aleatórios
# Usando funções nativas do Spark para evitar problemas de versão Python
df_nomes = df_nomes.withColumn("rand_escolaridade", rand()) \
    .withColumn("Escolaridade", 
        when(col("rand_escolaridade") < 0.33, "Fundamental")
        .when(col("rand_escolaridade") < 0.66, "Medio")
        .otherwise("Superior")
    ).drop("rand_escolaridade")

print("\nApós adicionar Escolaridade:")
df_nomes.show(10)

# Etapa 4: Adicionar coluna "Pais" com países da América do Sul
df_nomes = df_nomes.withColumn("rand_pais", rand()) \
    .withColumn("Pais",
        when(col("rand_pais") < 0.077, "Argentina")
        .when(col("rand_pais") < 0.154, "Bolivia")
        .when(col("rand_pais") < 0.231, "Brasil")
        .when(col("rand_pais") < 0.308, "Chile")
        .when(col("rand_pais") < 0.385, "Colombia")
        .when(col("rand_pais") < 0.462, "Ecuador")
        .when(col("rand_pais") < 0.539, "Guiana")
        .when(col("rand_pais") < 0.616, "Paraguay")
        .when(col("rand_pais") < 0.693, "Peru")
        .when(col("rand_pais") < 0.770, "Suriname")
        .when(col("rand_pais") < 0.847, "Uruguay")
        .when(col("rand_pais") < 0.924, "Venezuela")
        .otherwise("Guiana Francesa")
    ).drop("rand_pais")

print("\nApós adicionar Pais:")
df_nomes.show(10)

# Etapa 5: Adicionar coluna "AnoNascimento" (1945-2010)
# Gerar anos aleatórios entre 1945 e 2010 usando funções nativas
df_nomes = df_nomes.withColumn("AnoNascimento", 
    (floor(rand() * 66) + 1945).cast("int")  # 66 anos de diferença (2010-1945+1)
)

print("\nApós adicionar AnoNascimento:")
df_nomes.show(10)

# Etapa 6: Selecionar pessoas nascidas neste século (2001-2010)
df_select = df_nomes.filter(col("AnoNascimento") >= 2001)

print("\nPessoas nascidas neste século:")
df_select.show(10)

# Etapa 7: Registrar tabela temporária e executar SQL
df_nomes.createOrReplaceTempView("pessoas")

resultado_sql = spark.sql("select * from pessoas")
print("\nResultado do SQL:")
resultado_sql.show()

# Etapa 8: Filtrar Millennials (nascidos entre 1980 e 1994)
millennials = df_nomes.filter((col("AnoNascimento") >= 1980) & (col("AnoNascimento") <= 1994))

print(f"\nNúmero de Millennials: {millennials.count()}")
millennials.show()

# Etapa 9: Repetir processo da etapa 8 usando Spark SQL
millennials_sql = spark.sql("""
    SELECT * FROM pessoas 
    WHERE AnoNascimento >= 1980 AND AnoNascimento <= 1994
""")

print(f"\nMillennials usando SQL - Quantidade: {millennials_sql.count()}")
millennials_sql.show()

# Etapa 10: Obter quantidade de pessoas por país e geração
resultado_geracao = spark.sql("""
    SELECT 
        Pais,
        CASE 
            WHEN AnoNascimento BETWEEN 1944 AND 1964 THEN 'Baby Boomers'
            WHEN AnoNascimento BETWEEN 1965 AND 1979 THEN 'Geração X'
            WHEN AnoNascimento BETWEEN 1980 AND 1994 THEN 'Millennials'
            WHEN AnoNascimento BETWEEN 1995 AND 2015 THEN 'Geração Z'
            ELSE 'Outra'
        END as Geracao,
        COUNT(*) as Quantidade
    FROM pessoas
    GROUP BY Pais, 
        CASE 
            WHEN AnoNascimento BETWEEN 1944 AND 1964 THEN 'Baby Boomers'
            WHEN AnoNascimento BETWEEN 1965 AND 1979 THEN 'Geração X'
            WHEN AnoNascimento BETWEEN 1980 AND 1994 THEN 'Millennials'
            WHEN AnoNascimento BETWEEN 1995 AND 2015 THEN 'Geração Z'
            ELSE 'Outra'
        END
    ORDER BY Pais, Geracao, Quantidade DESC
""")

print("\nQuantidade de pessoas por País e Geração:")
resultado_geracao.show(50)

print("\nResumo das gerações:")
print("Baby Boomers — nascidos entre 1944 e 1964")
print("Geração X — nascidos entre 1965 e 1979") 
print("Millennials (Geração Y) — nascidos entre 1980 e 1994")
print("Geração Z — nascidos entre 1995 e 2015")

# Finalizar sessão Spark
# spark.stop()