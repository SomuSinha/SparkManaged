# Databricks notebook source
# MAGIC %md
# MAGIC # Math Functions and Simple Arithmetic
# MAGIC
# MAGIC #### Resources:
# MAGIC * Math Functions: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html#math-functions

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

# Simple arithmetic to return the population in milions
countries.select(countries['population']/1000000).withColumnRenamed('(population / 1000000)','population_m').display()

# COMMAND ----------

# Adding the column to a variable
countries_2 = countries.select(countries['population']/1000000).withColumnRenamed('(population / 1000000)','population_m')

# COMMAND ----------

countries_2.display()

# COMMAND ----------

# Using the round function to round to 3 decimal places
from pyspark.sql.functions import round
countries_2.select(round(countries_2['population_m'],3)).display()

# COMMAND ----------

# Rounding to 1dp
countries.withColumn('population_m', round(countries['population']/1000000,1)).display()