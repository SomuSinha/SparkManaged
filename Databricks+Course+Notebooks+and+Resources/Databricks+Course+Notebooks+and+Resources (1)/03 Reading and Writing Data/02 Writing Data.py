# Databricks notebook source
# MAGIC %md
# MAGIC # Writing Data
# MAGIC
# MAGIC #### Resources
# MAGIC * https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/io.html
# MAGIC * https://spark.apache.org/docs/latest/sql-data-sources-csv.html#data-source-option

# COMMAND ----------

# Defining the schema and importing Types 
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

# Reading in the countries.csv file
countries_df = spark.read.csv('/FileStore/tables/countries.csv', header=True, schema=countries_schema)

# COMMAND ----------

display(countries_df)

# COMMAND ----------

# Writing the countries_df Dataframe to the DBFS as a csv
countries_df.write.csv('/FileStore/tables/countries_out', header=True)

# COMMAND ----------

# Reading in the countries_out file
df = spark.read.csv('/FileStore/tables/countries_out', header=True)

# COMMAND ----------

display(df)

# COMMAND ----------

# Specifying the mode as overwrite allows you to overwrite an existing file
df.write.options(header=True).mode('overwrite').csv('/FileStore/tables/output/countries_out')

# COMMAND ----------

display(df)

# COMMAND ----------

# Partitioning the Dataframe file when writing it as a csv
df.write.options(header=True).mode('overwrite').partitionBy('REGION_ID','SUB_REGION_ID').csv('/FileStore/tables/countries_out')

# COMMAND ----------

# Reading an individual partition, you will need to pass in your specific file path
df2 = spark.read.csv('/FileStore/tables/countries_out/REGION_ID=10/part-00000-tid-7249390748988995848-2cdbc933-38c8-41ff-979e-8504e6f4a9dd-51-1.c000.csv', header=True)

# COMMAND ----------

display(df2)

# COMMAND ----------

# writing a csv file
df.write.mode('overwrite').partitionBy('REGION_ID','SUB_REGION_ID').csv('/FileStore/tables/countries_out_2', header=True)