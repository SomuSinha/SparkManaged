# Databricks notebook source
# MAGIC %md
# MAGIC # Union
# MAGIC
# MAGIC #### Resources:
# MAGIC * union: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.union.html?highlight=union#pyspark.sql.DataFrame.union

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

# Importing the count method and counting the number of records in the countries dataframe
from pyspark.sql.functions import count
countries.count()

# COMMAND ----------

# Performing a self union
countries.union(countries).count()

# COMMAND ----------

# Union only works with tables containing the same number of columns
countries.union(countries.drop('region_id'))