# Databricks notebook source
# MAGIC %md
# MAGIC # Filtering Dataframes
# MAGIC
# MAGIC #### Resources
# MAGIC * filter: https://spark.apache.org/docs/latest/api/python/reference/pyspark.pandas/api/pyspark.pandas.DataFrame.filter.html?highlight=filter#pyspark.pandas.DataFrame.filter
# MAGIC * Operators for conditional statements: https://spark.apache.org/docs/2.3.0/api/sql/index.html

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

# Using the filter method to filter records where populaton is less than 1000000000
countries.filter(countries['population']>1000000000).display()

# COMMAND ----------

# Using the locate function inside the filter condition
from pyspark.sql.functions import locate
countries.filter(locate("B", countries['capital'])==1).display()

# COMMAND ----------

# Using multiple conditions with the OR '|' Pipe Operator
countries.filter(  (locate("B", countries['capital'])==1) | (countries['population']>1000000000)    ).display()

# COMMAND ----------

# Using the not if condition
countries.filter("region_id != 10 and population ==0").display()

# COMMAND ----------

# Impporting the length function
from pyspark.sql.functions import length

# COMMAND ----------

# Using 'AND' condition via & operator
countries.filter( (length(countries['name']) > 15) & (countries['region_id'] != 10 )  ).display()

# COMMAND ----------

# Using SQL syntax in the filter method
countries.filter("length(name)>15 and region_id != 10").display()