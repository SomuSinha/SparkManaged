# Databricks notebook source
# MAGIC %md
# MAGIC # Managed Tables
# MAGIC
# MAGIC #### Resources:
# MAGIC * Managed Tables: https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/create-tables#--managed-tables
# MAGIC * SQL Syntax: https://spark.apache.org/docs/3.0.0-preview/sql-ref-syntax.html
# MAGIC * saveAsTable: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameWriter.saveAsTable.html?highlight=saveastable#pyspark.sql.DataFrameWriter.saveAsTable

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT current_database()

# COMMAND ----------

# MAGIC %sql
# MAGIC USE countries;

# COMMAND ----------

# MAGIC %sql
# MAGIC Show tables

# COMMAND ----------

# MAGIC %sql
# MAGIC describe extended countries_txt

# COMMAND ----------

# MAGIC %sql
# MAGIC drop table countries_txt

# COMMAND ----------

countries = spark.read.csv('/FileStore/tables/countries.csv', header=True)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT current_database()

# COMMAND ----------

# MAGIC %sql
# MAGIC USE default

# COMMAND ----------

countries.write.saveAsTable('countries.countries_mt')

# COMMAND ----------

# MAGIC %sql
# MAGIC describe extended countries.countries_mt

# COMMAND ----------

# MAGIC %sql
# MAGIC drop table countries.countries_mt

# COMMAND ----------

# MAGIC %sql
# MAGIC  
# MAGIC CREATE TABLE countries.countries_mt_empty
# MAGIC (country_id int,
# MAGIC name string,
# MAGIC nationality string,
# MAGIC country_code string,
# MAGIC iso_alpha_2 string,
# MAGIC capital string,
# MAGIC population int,
# MAGIC area_km2 int,
# MAGIC region_id int,
# MAGIC sub_region_id int,
# MAGIC intermediate_region_id int,
# MAGIC organization_region_id int)
# MAGIC USING CSV

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from countries.countries_mt_empty

# COMMAND ----------

# MAGIC %sql
# MAGIC create table countries.countries_copy as select * from countries.countries_mt

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from countries.countries_copy

# COMMAND ----------

# MAGIC %sql
# MAGIC describe extended countries.countries_copy

# COMMAND ----------

# MAGIC %sql
# MAGIC drop table countries.countries_copy

# COMMAND ----------

