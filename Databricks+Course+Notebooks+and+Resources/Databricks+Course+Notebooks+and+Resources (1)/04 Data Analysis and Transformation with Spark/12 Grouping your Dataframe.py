# Databricks notebook source
# MAGIC %md
# MAGIC # Grouping your Dataframe
# MAGIC
# MAGIC #### Resources:
# MAGIC * Grouping: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/grouping.html
# MAGIC * Aggregate Functions: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html#aggregate-functions

# COMMAND ----------

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

# Using the groupBy method
countries.groupBy('region_id')

# COMMAND ----------

# Importing all functions and aggregating the grouped Dataframe
from pyspark.sql.functions import *
countries. \
groupBy('region_id'). \
sum('population', 'area_km2'). \
display()

# COMMAND ----------

# Use the agg function for multiple aggregations
countries.groupBy('region_id').agg(avg('population'), sum('area_km2')).display()

# COMMAND ----------

# Use the agg function for multiple aggregations
countries.groupBy('region_id', 'sub_region_id').agg(avg('population'), sum('area_km2')).display()

# COMMAND ----------

# Using withColumnRenamed
countries.groupBy('region_id', 'sub_region_id'). \
agg(sum('population'), sum('area_km2')). \
withColumnRenamed('sum(population)', 'total_pop'). \
withColumnRenamed('sum(area_km2)', 'total_area'). \
display()


# COMMAND ----------

# Using alias
countries.groupBy('region_id', 'sub_region_id'). \
agg(sum('population').alias('total_pop'), sum('area_km2').alias('total_area')). \
display()

# COMMAND ----------

# Use the sort function to sort the resulting Dataframe
countries.groupBy('region_id', 'sub_region_id'). \
agg(max('population').alias('max_pop'), min('population').alias('min_pop')). \
sort(countries['region_id'].asc()). \
display()