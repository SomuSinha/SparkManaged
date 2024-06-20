# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC # Links and Resources
# MAGIC
# MAGIC * User Defined Functions: https://learn.microsoft.com/en-us/azure/databricks/udf/
# MAGIC * Spark Length Function: https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.functions.length.html
# MAGIC * Python Len Function: https://docs.python.org/3/library/functions.html

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

# COMMAND ----------

df = spark.read.csv('/FileStore/tables/bronze/customers.csv', header=True, inferSchema=True)
df.display()

# COMMAND ----------

df.withColumn('full_name_len', count_chars(df.FULL_NAME)).display()

# COMMAND ----------

# In order to use the count_chars_python function it needs to be declared as a udf
df.withColumn('full_name_len', count_chars_python(df.FULL_NAME)).display()

# COMMAND ----------

# declaring the udf
count_chars_python = udf(count_chars_python)

# COMMAND ----------

# The function now works in Spark DataFrames as it has been declared as a UDF
df.withColumn('full_name_len', count_chars_python(df.FULL_NAME)).display()