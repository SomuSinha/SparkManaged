# Databricks notebook source
# MAGIC %md
# MAGIC # Joining Dataframes
# MAGIC
# MAGIC #### Resources:
# MAGIC * join: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.join.html?highlight=join#pyspark.sql.DataFrame.join

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

# Reading in the regions csv file
regions_path = '/FileStore/tables/country_regions.csv'
 
regions_schema = StructType([
                    StructField("Id", StringType(), False),
                    StructField("NAME", StringType(), False)
                    ]
                    )
 
regions = spark.read.csv(path=regions_path, header=True, schema=regions_schema)

# COMMAND ----------

countries.display()

# COMMAND ----------

regions.display()

# COMMAND ----------

# Joining the countries and regions dataframes
countries.join(regions, countries['region_id']==regions['Id'], 'right').display()

# COMMAND ----------

# Joining and sorting the countries and regions dataframes, also selecting only specific columns
countries. \
join(regions, regions['Id']==countries['region_id'], 'inner'). \
select(countries['name'].alias('country_name'), regions['name'].alias('region_name'), countries['population']). \
sort(countries['population'].desc()). \
display()