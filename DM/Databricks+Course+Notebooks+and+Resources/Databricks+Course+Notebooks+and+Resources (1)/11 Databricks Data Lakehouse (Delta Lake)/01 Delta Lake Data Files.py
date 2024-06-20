# Databricks notebook source
# MAGIC %md
# MAGIC # Delta Lake Files
# MAGIC
# MAGIC #### Resources
# MAGIC * DataFrameReader.format: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.format.html#pyspark.sql.DataFrameReader.format
# MAGIC * DataFrameWriter.format: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameWriter.format.html#pyspark.sql.DataFrameWriter.format

# COMMAND ----------

# Use databricks backed secret scopes to retrieve the IDs and secret, store the relevant values into variables
application_id = dbutils.secrets.get(scope="databricks-secrets-639", key="application-id")
tenant_id = dbutils.secrets.get(scope="databricks-secrets-639", key="tenant-id")
secret = dbutils.secrets.get(scope="databricks-secrets-639", key="secret")

container_name = 'delta-lake-demo'
mount_point = '/mnt/delta-lake-demo'
account_name = 'datalake639'

# COMMAND ----------

# Mount the empty container
configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": application_id,
          "fs.azure.account.oauth2.client.secret": secret,
          "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"}

# Optionally, you can add <directory-name> to the source URI of your mount point.
dbutils.fs.mount(
  source = f"abfss://{container_name}@{account_name}.dfs.core.windows.net/",
  mount_point = mount_point,
  extra_configs = configs)

# COMMAND ----------

# Mounting the bronze container (if it's not already mounted)
application_id = dbutils.secrets.get(scope="databricks-secrets-639", key="application-id")
tenant_id = dbutils.secrets.get(scope="databricks-secrets-639", key="tenant-id")
secret = dbutils.secrets.get(scope="databricks-secrets-639", key="secret")

container_name = 'bronze'
mount_point = '/mnt/bronze'
account_name = 'datalake639'

# COMMAND ----------

# Mount the bronze container
configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": application_id,
          "fs.azure.account.oauth2.client.secret": secret,
          "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"}

# Optionally, you can add <directory-name> to the source URI of your mount point.
dbutils.fs.mount(
  source = f"abfss://{container_name}@{account_name}.dfs.core.windows.net/",
  mount_point = mount_point,
  extra_configs = configs)

# COMMAND ----------

# Reading in the countries.csv file from the bronze container and assigning it to a variable
countries = spark.read.csv("/mnt/bronze/countries.csv", header=True, inferSchema=True)

# COMMAND ----------

countries.display()

# COMMAND ----------

# Saving the countries dataframe as a parquet file in the delta-lake-demo container
countries.write.format("delta").save('/mnt/delta-lake-demo/coutries_delta')

# COMMAND ----------

# Saving the countries dataframe as a parquet file in the delta-lake-demo container, notice the difference, there is no transaction log
countries.write.format("parquet").save('/mnt/delta-lake-demo/countries_parquet')

# COMMAND ----------

spark.read.format("delta").load("/mnt/delta-lake-demo/coutries_delta").display()

# COMMAND ----------

# You can partition and overwrite just as with a parquet or other file format
countries.write.format("delta").mode("overwrite").partitionBy("REGION_ID").save("/mnt/delta-lake-demo/coutries_delta_part")

# COMMAND ----------

countries.display()

# COMMAND ----------

# MAGIC %md 
# MAGIC ## Managed and External Tables

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE delta_lake_db;

# COMMAND ----------

# Creating a managed table on the delta_lake_db database
countries = spark.read.format("delta").load("/mnt/delta-lake-demo/coutries_delta")

# COMMAND ----------

# Creating an external table on the delta_lake_db database
countries.write.saveAsTable("delta_lake_db.countries_managed_delta")

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED delta_lake_db.countries_managed_delta

# COMMAND ----------

countries.write.option("path", "/mnt/delta-lake-demo/countries_delta").saveAsTable("delta_lake_db.countries_ext_delta")

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED delta_lake_db.countries_managed_delta