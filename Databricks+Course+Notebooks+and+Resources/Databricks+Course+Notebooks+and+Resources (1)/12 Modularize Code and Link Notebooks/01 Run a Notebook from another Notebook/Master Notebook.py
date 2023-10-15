# Databricks notebook source
# MAGIC %md
# MAGIC # Master Notebook
# MAGIC
# MAGIC ### This notebook is running the worker notebook
# MAGIC
# MAGIC
# MAGIC ### References:
# MAGIC * https://learn.microsoft.com/en-us/azure/databricks/notebooks/notebook-workflows

# COMMAND ----------

# Running the worker notebook in the same folder by referencing workbook name
dbutils.notebook.run('Worker Notebook', 60)

# COMMAND ----------

# Copy in the file path if the workbook is saved elsewhere
dbutils.notebook.run('COPY FILEPATH OF NOTEBOOK HERE', 60)

# COMMAND ----------

# Use a try except block to handle errors
try:
    dbutils.notebook.run('Worker Notebook', 60)
except:
    print("Error occured")

# COMMAND ----------

# Running the notebook and passing in arguments for the worker notebooks text widget
dbutils.notebook.run('Worker Notebook', 60, {'input_widget': 'From Master Notebook'})