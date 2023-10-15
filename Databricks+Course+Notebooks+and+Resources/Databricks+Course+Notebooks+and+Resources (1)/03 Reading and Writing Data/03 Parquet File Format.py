# Databricks notebook source
# MAGIC %md
# MAGIC # Parquet File Format
# MAGIC
# MAGIC #### Resources
# MAGIC * https://learn.microsoft.com/en-us/azure/databricks/external-data/parquet

# COMMAND ----------

# Reading a csv file into a Dataframe
df = spark.read.csv('/FileStore/tables/countries.csv', inferSchema=True, header=True)

# COMMAND ----------

display(df)

# COMMAND ----------

# Writing a file as parquet format
df.write.parquet('/FileStore/tables/output/countries_parquet')

# COMMAND ----------

# Reading the results via display
display(spark.read.parquet('/FileStore/tables/output/countries_parquet'))