# Databricks notebook source
# MAGIC %md
# MAGIC # Perform SQL queries on Dataframes
# MAGIC
# MAGIC #### Resources
# MAGIC * createTempView: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.createTempView.html?highlight=createtemp
# MAGIC * createOrReplaceTempView: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.createOrReplaceTempView.html#pyspark.sql.DataFrame.createOrReplaceTempView
# MAGIC * createGlobalTempView: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.createGlobalTempView.html#pyspark.sql.DataFrame.createGlobalTempView
# MAGIC * createOrReplaceGlobalTempView: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.createOrReplaceGlobalTempView.html#pyspark.sql.DataFrame.createOrReplaceGlobalTempView
# MAGIC * spark.sql: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.sql.html#pyspark.sql.SparkSession.sql

# COMMAND ----------

# Reading the countries csv file into a dataframe
countries = spark.read.csv('/FileStore/tables/countries.csv', header=True)

# COMMAND ----------

countries.display()

# COMMAND ----------

# You cannot use SQL on the file path to reference the data
%sql
SELECT * FROM '/FileStore/tables/countries.csv';

# COMMAND ----------

# Creating a temp view from the dataframe
countries.createTempView('countries_tv')

# COMMAND ----------

# Performing SQL on the temp view
%sql
select * from countries_tv

# COMMAND ----------

# Writing SQL on a Python cell via spark.sql
spark.sql("select * from countries_tv").display()

# COMMAND ----------

table_name = 'countries_tv'

# COMMAND ----------

# spark.sql allows use of f strings to pass in expressions and variables
spark.sql(f"select * from {table_name}").display()

# COMMAND ----------

# Temp view cannot be accessed outside of the session and notebook
countries.createOrReplaceTempView('countries_tv')

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select * from countries_tv

# COMMAND ----------

# Global temp views can be accessed outside of the current notebook
countries.createOrReplaceGlobalTempView('countries_gv')

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from global_temp.countries_gv