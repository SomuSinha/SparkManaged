# Databricks notebook source
# MAGIC %md
# MAGIC # Unpivotting Dataframes

# COMMAND ----------

# Reading the countries csv file into a dataframe
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

# Reading the regions csv file into a dataframe
regions_path = '/FileStore/tables/country_regions.csv'
 
regions_schema = StructType([
                    StructField("Id", StringType(), False),
                    StructField("NAME", StringType(), False)
                    ]
                    )
 
regions = spark.read.csv(path=regions_path, header=True, schema=regions_schema)

# COMMAND ----------

# joining the countries and regions dataframes
countries = countries.join(regions,countries['region_id']==regions['Id'], 'inner').select(countries['name'].alias('country_name'), regions['name'].alias('region_name'),countries['population'])

# COMMAND ----------

countries.display()

# COMMAND ----------

# Grouping and pivotting the resulting joined countries dataframe
pivot_countries = countries.groupBy('country_name').pivot('region_name').sum('population')

# COMMAND ----------

pivot_countries.display()

# COMMAND ----------

# Using SQL syntax to unpivot the dataframe
from pyspark.sql.functions import expr

pivot_countries.select('country_name', expr("stack(5, 'Africa', Africa, 'America', America, 'Asia', Asia, 'Europe', Europe,'Oceania', Oceania) as (region_name, population)")).filter('population is not null').display()