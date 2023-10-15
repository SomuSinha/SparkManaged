# Databricks notebook source
# MAGIC %md
# MAGIC # Permanent Views
# MAGIC
# MAGIC #### Resources:
# MAGIC * Create View: https://spark.apache.org/docs/3.0.0-preview/sql-ref-syntax-ddl-create-view.html

# COMMAND ----------

countries = spark.read.csv('/FileStore/tables/countries.csv', header=True)

# COMMAND ----------

# MAGIC %sql
# MAGIC use countries

# COMMAND ----------

countries.write.saveAsTable('countries_mt')

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from countries_mt

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW countries.view_region_10
# MAGIC AS SELECT * FROM countries.countries_mt 
# MAGIC WHERE region_id = 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from view_region_10

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC drop database countries cascade;