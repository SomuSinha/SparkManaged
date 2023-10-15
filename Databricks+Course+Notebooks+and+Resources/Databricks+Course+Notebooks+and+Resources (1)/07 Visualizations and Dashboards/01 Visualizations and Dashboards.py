# Databricks notebook source
# MAGIC %md
# MAGIC # Visualizations and Dashboards
# MAGIC
# MAGIC #### Resources:
# MAGIC * Visualizations: https://learn.microsoft.com/en-us/azure/databricks/notebooks/visualizations/
# MAGIC * Dashboards: https://learn.microsoft.com/en-us/azure/databricks/notebooks/dashboards

# COMMAND ----------

# Reading in the order_details and monthly_sales parquet files
# Change your filepath accordingly
order_details = spark.read.parquet("/FileStore/tables/gold/order_details")
monthly_sales = spark.read.parquet("/FileStore/tables/gold/monthly_sales")

# COMMAND ----------

# Using the display function allows you to create visuals
display(order_details)

# COMMAND ----------

display(monthly_sales)

# COMMAND ----------

# MAGIC %md
# MAGIC Some text for my notebook

# COMMAND ----------

# MAGIC %md
# MAGIC # Title for my dashboard

# COMMAND ----------

# You can add HTML titles and text to your dashboard
displayHTML("""<font size="6" color="red" face="sans-serif">Sales Dashboard</font>""")