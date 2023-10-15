# Databricks notebook source
# MAGIC %md
# MAGIC # Worker Notebook
# MAGIC
# MAGIC ### This notebook can be run via the Master notebook
# MAGIC
# MAGIC
# MAGIC ### References:
# MAGIC * https://learn.microsoft.com/en-us/azure/databricks/notebooks/notebook-workflows

# COMMAND ----------

print("Printed from Worker Notebook")

# COMMAND ----------

# Creating a text widget
dbutils.widgets.text('input_widget', '', 'provide an input')

# COMMAND ----------

# Retrieving the widget value
dbutils.widgets.get('input_widget')

# COMMAND ----------

# Exit must be on the last cell
dbutils.notebook.exit("Worker Notebook Executed Successfully")