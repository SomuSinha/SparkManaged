# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC # Links and Resources
# MAGIC
# MAGIC * User Defined Functions: https://learn.microsoft.com/en-us/azure/databricks/udf/

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# This function is defined using native Spark
def count_chars(col):
    return length(col)

# COMMAND ----------

# This function is defined using pure Python
def count_chars_python(col):
    return len(col)

# Declaring the UDF
count_chars_python = udf(count_chars_python)

# COMMAND ----------

df = spark.read.csv('/FileStore/tables/bronze/customers.csv', header=True, inferSchema=True)
df.display()

# COMMAND ----------

df.count()

# COMMAND ----------

# Unioning the dataframe to increase row count
new_df = df

for _ in range(100):
    df = df.union(new_df)

df.count()

# COMMAND ----------

# Native spark function will execute faster
df.withColumn('full_name_length', count_chars(df.FULL_NAME))

# COMMAND ----------

# The python UDF will take longer to execute due to added overhead
df.withColumn('full_name_length', count_chars_python(df.FULL_NAME))