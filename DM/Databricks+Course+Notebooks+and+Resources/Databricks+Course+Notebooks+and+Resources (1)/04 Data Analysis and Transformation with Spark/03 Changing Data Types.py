# Databricks notebook source
# MAGIC %md
# MAGIC # Changing Data Types
# MAGIC
# MAGIC #### Resources:
# MAGIC * data types in spark: https://spark.apache.org/docs/latest/sql-ref-datatypes.html
# MAGIC * cast: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.Column.cast.html?highlight=cast#pyspark.sql.Column.cast

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

countries.dtypes

# COMMAND ----------

# Reading the countries file without specifying the schema, into a new variable
countries_dt = spark.read.csv(path=countries_path, header=True)

# COMMAND ----------

# Note the data types are all string
countries_dt.dtypes

# COMMAND ----------

# Using the cast method to cast the population column as IntegerType(), IntegerType() has already been imported in the first cell
countries_dt.select(countries_dt['population'].cast(IntegerType())).dtypes

# COMMAND ----------

# Using the cast method to cast the population column as StringType(), StringType() has already been imported in the first cell
countries.select(countries['population'].cast(StringType())).dtypes