# Databricks notebook source
# MAGIC %md
# MAGIC # Updating and Deleting Records
# MAGIC
# MAGIC #### Resources:
# MAGIC * https://docs.delta.io/0.5.0/delta-update.html

# COMMAND ----------

# MAGIC %md
# MAGIC ### Deleting Records

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED delta_lake_db.countries_managed_delta

# COMMAND ----------

countries = spark.read.csv("/mnt/bronze/countries.csv", header=True, inferSchema=True)

# COMMAND ----------

# Creating an externally managed parquet table
countries.write.format("parquet").saveAsTable("delta_lake_db.countries_managed_pq")

# COMMAND ----------

# Can confirm the countries_maanged_pq table is managed parquet by using describe extended

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED delta_lake_db.countries_managed_pq

# COMMAND ----------

# similarly the countries managed delta file is a delta format managed table

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED delta_lake_db.countries_managed_delta

# COMMAND ----------

# You can list all of the databases by doing show databases

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SHOW DATABASES;

# COMMAND ----------

# I'll use delta_lake_db to avoid qualifying table names

# COMMAND ----------

# MAGIC %sql
# MAGIC USE delta_lake_db

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM countries_managed_pq

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM countries_managed_delta

# COMMAND ----------

# Delete operations or DML operations don't work on other file formats such as parquet

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC DELETE FROM countries_managed_pq WHERE region_id = 50;

# COMMAND ----------

# Delete operations and DML DO work on delta tables

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC DELETE FROM countries_managed_delta WHERE region_id = 50;

# COMMAND ----------

# The changes are applied to the underlying data as expected

# COMMAND ----------

spark.read.format("delta").load("/user/hive/warehouse/delta_lake_db.db/countries_managed_delta").display()

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM countries_managed_delta
# MAGIC WHERE region_id = 50

# COMMAND ----------

# Delete using Python code
# First create a deltaTable object and import libraries and functions
from delta.tables import *
from pyspark.sql.functions import *

deltaTable = DeltaTable.forPath(spark, "/user/hive/warehouse/delta_lake_db.db/countries_managed_delta")

# COMMAND ----------

# Delete using SQL formatted string
deltaTable.delete("region_id = 20")        # predicate using SQL formatted string

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM countries_managed_delta
# MAGIC WHERE region_id = 20

# COMMAND ----------

# Delete using SQL formatted string
deltaTable.delete("region_id = 30 and area_km2 >100000")        # predicate using SQL formatted string

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM countries_managed_delta

# COMMAND ----------

# Delete using Spark SQL
deltaTable.delete( col("country_code") == 'XXX' )   # predicate using Spark SQL functions

# COMMAND ----------

# MAGIC %md
# MAGIC ### Updating Records

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM countries_managed_delta;

# COMMAND ----------

# Update using SQL cell

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC UPDATE countries_managed_delta 
# MAGIC SET country_code = 'XXX'
# MAGIC WHERE region_id=10

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM countries_managed_delta;

# COMMAND ----------

# Delete using SQL formatted string
deltaTable.update("region_id = '30'", { "country_code": "'XXX'" } )   # predicate using SQL formatted string

# COMMAND ----------

# Delete using Spark SQL
deltaTable.update(col("region_id")==30, { "country_code": lit("XXX") } )   # predicate using Spark SQL functions

# COMMAND ----------

# Delete using SQL formatted string and multiple conditions
deltaTable.update(
  condition = "region_id = 30 and area_km2>500000",
  set = { "country_code": "'YYY'" }
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM countries_managed_delta;