# Databricks notebook source
# MAGIC %md
# MAGIC # Hive Metastore and Creating Databases
# MAGIC
# MAGIC #### Resources
# MAGIC * Hive Metastore: https://docs.databricks.com/data/metastores/index.html
# MAGIC * Creating Databases: https://spark.apache.org/docs/3.0.0-preview/sql-ref-syntax-ddl-create-database.html

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS countries

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP DATABASE IF EXISTS countries;