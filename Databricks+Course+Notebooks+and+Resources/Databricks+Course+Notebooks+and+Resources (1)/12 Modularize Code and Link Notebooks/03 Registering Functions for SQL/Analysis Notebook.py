# Databricks notebook source
# The %run magic command allows you to include another notebook within the calling notebook

# COMMAND ----------

# MAGIC %run "./Utility Notebook"

# COMMAND ----------

df = spark.read.csv('/FileStore/tables/bronze/order_items.csv', header=True, inferSchema=True)
df.display()

# COMMAND ----------

df.createOrReplaceTempView('temp')

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from temp;

# COMMAND ----------

# MAGIC %md
# MAGIC To run the below cell you need to register the function (see Utility Notebook)

# COMMAND ----------

# MAGIC %sql
# MAGIC select *, multiply_cols(unit_price, quantity) as line_amount from temp;