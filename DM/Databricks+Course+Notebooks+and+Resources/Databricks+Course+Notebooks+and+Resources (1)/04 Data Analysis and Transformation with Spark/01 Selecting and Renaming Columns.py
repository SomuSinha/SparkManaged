# Databricks notebook source
# MAGIC %md
# MAGIC # Selecting and Renaming Columns
# MAGIC
# MAGIC #### Resources
# MAGIC * select: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.select.html?highlight=select#pyspark.sql.DataFrame.select
# MAGIC * col: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.col.html?highlight=col#pyspark.sql.functions.col
# MAGIC * alias: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.Column.alias.html?highlight=alias#pyspark.sql.Column.alias
# MAGIC * withColumnRenamed: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.withColumnRenamed.html?highlight=withcolumnrenamed#pyspark.sql.DataFrame.withColumnRenamed

# COMMAND ----------

# Reading in the countries csv file as a Dataframe
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

countries = spark.read.csv(path=countries_path, header = True, schema=countries_schema)

# COMMAND ----------

countries.display()

# COMMAND ----------

# You can select columns by using the select method and specifying the column names
countries.select('NAME', 'capital', 'population').display()

# COMMAND ----------

# You can also provide the columns by specifically referring to the dataframe and passing the column name inside of the square brackets, this allows you to perform additonal methods on the columns
countries.select(countries['NAME'], countries['capital'], countries['population']).display()

# COMMAND ----------

# You can also provide the columns by qualifying the column name with the Dataframe, this allows you to perform additonal methods on the columns
countries.select(countries.NAME, countries.CAPITAL, countries.POPULATION).display()

# COMMAND ----------

# Importing the col function
from pyspark.sql.functions import col

countries.select(col('name'), col('capital'), col('population')).display()

# COMMAND ----------

# The alias method allows you to rename the columns
countries.select(countries['name'].alias('country_name'), countries['capital'].alias('capital_city'), countries['population']).display()

# COMMAND ----------

# withColumnRenamed allows you to rename a column
countries.select('name', 'capital', 'population').withColumnRenamed('name', 'country_name').withColumnRenamed('capital', 'capital_city').display()

# COMMAND ----------

# Reading in the regions.csv file and assiging it to a variable
regions_path = '/FileStore/tables/country_regions.csv'

regions_schema = StructType([
    StructField('Id', StringType(), False),
    StructField('NAME', StringType(), False)
])

regions = spark.read.csv(path = regions_path, header=True, schema=regions_schema)

# COMMAND ----------

regions.display()

# COMMAND ----------

# aliasing the column 'name' to 'continent' with alias
regions.select(regions['Id'], regions['name'].alias('continent')).display()

# COMMAND ----------

# aliasing the column 'name' to 'continent' with withColumnRenamed
regions.select(regions['Id'], regions['name']).withColumnRenamed('name', 'continent').display()