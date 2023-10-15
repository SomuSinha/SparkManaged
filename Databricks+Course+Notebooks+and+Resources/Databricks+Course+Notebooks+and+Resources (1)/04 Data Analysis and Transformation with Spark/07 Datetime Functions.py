# Databricks notebook source
# MAGIC %md
# MAGIC # Datetime Functions
# MAGIC
# MAGIC #### Resources
# MAGIC * Datetime Functions: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html#datetime-functions
# MAGIC * Datetime Patterns: https://spark.apache.org/docs/latest/sql-ref-datetime-pattern.html

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

countries.display()

# COMMAND ----------

# Importing all functions and using current_timestamp and withColumn
from pyspark.sql.functions import *
countries = countries.withColumn('timestamp', current_timestamp())

# COMMAND ----------

countries.display()

# COMMAND ----------

# Using year to extract the year
countries.select(year(countries['timestamp'])).display()

# COMMAND ----------

countries = countries.withColumn('date_literal', lit('27-10-2020'))

# COMMAND ----------

countries.display()

# COMMAND ----------

countries.dtypes

# COMMAND ----------

# Using the to_date function to convert a string to a date
countries = countries.withColumn('date', to_date(countries['date_literal'],'dd-MM-yyyy'))

# COMMAND ----------

countries.display()

# COMMAND ----------

countries.dtypes