# Databricks notebook source
# The %run magic command allows you to include another notebook within the calling notebook

# COMMAND ----------

# MAGIC %run "./Utility Notebook"

# COMMAND ----------

# The dbutils.notebook.run method starts a new job to run the notebook. The functions defined in the Utility Notebook will not be available in this notebook
#dbutils.notebook.run('./Utility Notebook', 60)

# COMMAND ----------

df1 = spark.read.csv('/FileStore/tables/bronze/customers.csv', header=True, inferSchema=True)
df1.display()

df2 = spark.read.csv('/FileStore/tables/bronze/order_items.csv', header=True, inferSchema=True)
df2.display()

# COMMAND ----------

#The ingestion_date function is defined in the Utility Notebook and will not be usable until the %run operation is used on the Utility Notebook
add_ingestion_date(df1).display()