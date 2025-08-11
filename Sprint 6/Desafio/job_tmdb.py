import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Caminhos
raw_path = "s3://data-lake-isa1/Raw/TMDB/JSON/Movies/2025/07/28/"
trusted_path = "s3://data-lake-isa1/Trusted/Movies/JSON/"

# 1. Ler JSON da Raw Zone
df = spark.read.json(raw_path)

# 2. Limpeza e transformação
df = df.dropDuplicates().na.drop(how="all")
df = df.withColumn("processed_date", F.current_date()) \
       .withColumn("processed_timestamp", F.current_timestamp()) \
       .withColumn("data_source", F.lit("raw_tmdb_json")) \
       .withColumn("ano", F.year(F.current_date())) \
       .withColumn("mes", F.month(F.current_date())) \
       .withColumn("dia", F.dayofmonth(F.current_date()))

# 3. Escrever na Trusted Zone particionado por ano/mes/dia
dynamic_frame = DynamicFrame.fromDF(df, glueContext, "trusted_data")
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame,
    connection_type="s3",
    connection_options={
        "path": trusted_path,
        "partitionKeys": ["ano", "mes", "dia"]
    },
    format="parquet"
)

job.commit()