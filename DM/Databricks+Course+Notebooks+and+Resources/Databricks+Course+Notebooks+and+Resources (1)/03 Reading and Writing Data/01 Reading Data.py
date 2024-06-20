# Databricks notebook source
# MAGIC %md
# MAGIC # Reading Data
# MAGIC
# MAGIC #### Resources
# MAGIC * Input / Output: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/io.html
# MAGIC * Data Source Options: https://spark.apache.org/docs/latest/sql-data-sources-csv.html#data-source-option
# MAGIC * StructType: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.types.StructType.html#pyspark.sql.types.StructType
# MAGIC * StrcutField: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.types.StructField.html#pyspark.sql.types.StructField

# COMMAND ----------

# Reading a CSV file
# Ensure that your filepath is the same as the code below, otherwise paste in your file path inside of the parenthesis
spark.read.csv("/FileStore/tables/countries.csv")

# COMMAND ----------

# Loading a CSV file into the resulting Dataframe. 
# Ensure that your filepath is the same as the code below, otherwise paste in your file path inside of the parenthesis
countries_df = spark.read.csv("/FileStore/tables/countries.csv")

# COMMAND ----------

# Confirming the type of the object countries_df
type(countries_df)

# COMMAND ----------

# Using the display function to display the dataframe
display(countries_df)

# COMMAND ----------

# You can also use display as a method via dot notation
countries_df.display()

# COMMAND ----------

# Specifying the argument for header=True
countries_df = spark.read.csv("/FileStore/tables/countries.csv", header=True)

# COMMAND ----------

# Displaying the Dataframe, this time the first row has been read as a header
display(countries_df)

# COMMAND ----------

# Specifying the argument for header=True inside of the options method
countries_df = spark.read.options(header=True).csv('/FileStore/tables/countries.csv')

# COMMAND ----------

# Displaying the Dataframe
display(countries_df)

# COMMAND ----------

# Returning the data types
countries_df.dtypes

# COMMAND ----------

# Returning the schema
countries_df.schema

# COMMAND ----------

# Using the describe method
countries_df.describe()

# COMMAND ----------

# Using the inferSchema option as True
countries_df = spark.read.options(header=True, inferSchema=True).csv('/FileStore/tables/countries.csv')

# COMMAND ----------

# Importing Types and defining the schema before reading in the csv file
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


# COMMAND ----------

# Reading in the csv file and passing in the schema defined in the previous cell. Note the data types
countries_df = spark.read.csv('/FileStore/tables/countries.csv', header=True, schema=countries_schema)

# COMMAND ----------

# Alternative syntax for passing in the schema inside of the options method
countries_df = spark.read.options(header=True).schema(countries_schema).csv('/FileStore/tables/countries.csv')

# COMMAND ----------

# Reading in a single line json file
countries_sl_json = spark.read.json('/FileStore/tables/countries_single_line.json')

# COMMAND ----------

display(countries_sl_json)

# COMMAND ----------

# Reading in a multi line json file
countries_ml_json = spark.read.options(multiLine=True).json('/FileStore/tables/countries_multi_line.json')

# COMMAND ----------

display(countries_ml_json)

# COMMAND ----------

# Reading in a text file
countries_txt = spark.read.options(header=True, sep='\t').csv('/FileStore/tables/countries.txt')

# COMMAND ----------

display(countries_txt)