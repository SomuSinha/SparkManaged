# Databricks notebook source
# MAGIC %md
# MAGIC # Removing Columns
# MAGIC
# MAGIC #### Resources:
# MAGIC * select: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.select.html?highlight=select#pyspark.sql.DataFrame.select
# MAGIC * drop: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.drop.html?highlight=drop#pyspark.sql.DataFrame.drop

# COMMAND ----------

# Reading the countries csv file as a Dataframe
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

# Using the select method
countries_2 = countries.select('name','capital', 'population')

# COMMAND ----------

countries_2.display()

# COMMAND ----------

countries.display()

# COMMAND ----------

# Using the drop method
countries_3 = countries.drop(countries['organization_region_id'])

# COMMAND ----------

countries_3.display()

# COMMAND ----------

countries_3.drop('sub_region_id', 'intermediate_region_id').display()