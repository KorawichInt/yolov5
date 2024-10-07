import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_unixtime, col, to_timestamp
from pyspark.sql.types import DoubleType
import pandas as pd

# Create spark session
spark = (SparkSession
         .builder
         .getOrCreate()
         )

####################################
# Parameters
####################################
# movies_file = sys.argv[1]
# ratings_file = sys.argv[2]
gpt_prompt_file = sys.argv[1]
postgres_db = sys.argv[2]
postgres_user = sys.argv[3]
postgres_pwd = sys.argv[4]

####################################
# Read CSV Data
####################################
print("######################################")
print("READING CSV FILES")
print("######################################")

gpt_prompt_path = "/usr/local/spark/assets/data/detection_log.csv"
df = pd.read_csv(gpt_prompt_file)
df.to_csv(gpt_prompt_path)

df_gpt_prompt_csv = (
    spark.read
    .format("csv")
    .option("header", True)
    .load(gpt_prompt_path)
)

# df_movies_csv = (
#     spark.read
#     .format("csv")
#     .option("header", True)
#     .load(movies_file)
# )

# df_ratings_csv = (
#     spark.read
#     .format("csv")
#     .option("header", True)
#     .load(ratings_file)
#     .withColumnRenamed("timestamp", "timestamp_epoch")
# )

# Convert epoch to timestamp and rating to DoubleType
# df_ratings_csv_fmt = (
#     df_ratings_csv
#     .withColumn('rating', col("rating").cast(DoubleType()))
#     .withColumn('timestamp', to_timestamp(from_unixtime(col("timestamp_epoch"))))
# )

####################################
# Load data to Postgres
####################################
print("######################################")
print("LOADING POSTGRES TABLES")
print("######################################")

(
    df_gpt_prompt_csv.write
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.gpt_prompt")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .mode("overwrite")
    .save()
)

# (
#     df_movies_csv.write
#     .format("jdbc")
#     .option("url", postgres_db)
#     .option("dbtable", "public.movies")
#     .option("user", postgres_user)
#     .option("password", postgres_pwd)
#     .mode("overwrite")
#     .save()
# )

# (
#     df_ratings_csv_fmt
#     .select([c for c in df_ratings_csv_fmt.columns if c != "timestamp_epoch"])
#     .write
#     .format("jdbc")
#     .option("url", postgres_db)
#     .option("dbtable", "public.ratings")
#     .option("user", postgres_user)
#     .option("password", postgres_pwd)
#     .mode("overwrite")
#     .save()
# )
