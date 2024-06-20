# Databricks notebook source
# MAGIC %md
# MAGIC # String Functions
# MAGIC
# MAGIC #### Resources
# MAGIC * String Functions: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html#string-functions

# COMMAND ----------

# Reading in the countries csv file into a variable
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

# Importing all functions for simplicity
from pyspark.sql.functions import *

# COMMAND ----------

# Using the length function
countries.select(length(countries['name'])).display()

# COMMAND ----------

countries.display()

# COMMAND ----------

# Using concat_ws function to concatenate columns
countries.select(concat_ws('-', countries['name'], lower(countries['country_code']))).display()