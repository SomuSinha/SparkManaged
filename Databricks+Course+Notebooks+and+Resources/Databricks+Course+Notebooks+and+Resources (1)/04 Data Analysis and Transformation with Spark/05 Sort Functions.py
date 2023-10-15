# Databricks notebook source
# MAGIC %md
# MAGIC # Sort Functions
# MAGIC
# MAGIC #### Resources:
# MAGIC * Sort Functions: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html#sort-functions

# COMMAND ----------

# Reading in the countries.csv file and specifying the schema
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

countries.display()

# COMMAND ----------

# Importing asc to sort in ascending order
from pyspark.sql.functions import asc
countries.sort(countries['population'].asc()).display()

# COMMAND ----------

# Importing desc to sort in descending order
from pyspark.sql.functions import desc
countries.sort(countries['population'].desc()).display()