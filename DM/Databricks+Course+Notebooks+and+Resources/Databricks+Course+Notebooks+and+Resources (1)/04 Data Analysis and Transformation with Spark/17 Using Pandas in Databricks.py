# Databricks notebook source
# MAGIC %md
# MAGIC # Using Pandas in Databricks
# MAGIC
# MAGIC #### Resources:
# MAGIC * Pandas API on Spark: https://spark.apache.org/docs/latest/api/python/reference/pyspark.pandas/index.html

# COMMAND ----------

# Reading in the countries csv file
countries_path = '/FileStore/tables/countries.csv'

from pyspark.sql.types import IntegerType, StringType, DoubleType, StructField, StructType
countries_schema = StructType([
                    StructField("COUNTRY_ID", IntegerType(), False),
                    StructField("NAME", StringType(), False),
                    StructField("NATIONALITY", StringType(), False),
                    StructField("COUNTRY_CODE", StringType(), False),
                    StructField("ISO_ALPHA2", StringType(), False),
                    StructField("CAPITAL", StringType(), False),
                    StructField("POPULATION", DoubleType(), False),
                    StructField("AREA_KM2", IntegerType(), False),
                    StructField("REGION_ID", IntegerType(), True),
                    StructField("SUB_REGION_ID", IntegerType(), True),
                    StructField("INTERMEDIATE_REGION_ID", IntegerType(), True),
                    StructField("ORGANIZATION_REGION_ID", IntegerType(), True)
                    ]
                    )

countries=spark.read.csv(path=countries_path, header=True, schema=countries_schema)

# COMMAND ----------

# Importing the pandas library
import pandas as pd

# COMMAND ----------

# Converting a spark dataframe to a pandas dataframe using toPandas()
countries_pd = countries.toPandas()

# COMMAND ----------

# You can now use Pandas on the resulting dataframe
countries_pd.iloc[0]