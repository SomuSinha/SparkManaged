# Databricks notebook source
# MAGIC %md
# MAGIC # Deleting Files and Folders
# MAGIC
# MAGIC #### Resources:
# MAGIC * https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-utils

# COMMAND ----------

# Use dbutils.fs.help to get a list of methods available
dbutils.fs.help()

# COMMAND ----------

# Removing a file
dbutils.fs.rm('/FileStore/tables/countries.txt')

# COMMAND ----------

# Removing files
dbutils.fs.rm('/FileStore/tables/countries_multi_line.json')
dbutils.fs.rm('/FileStore/tables/countries_single_line.json')

# COMMAND ----------

# When deleting a folder you need to specify recurse=True to delete the contents of the folder
dbutils.fs.rm('/FileStore/tables/countries_out', recurse=True)