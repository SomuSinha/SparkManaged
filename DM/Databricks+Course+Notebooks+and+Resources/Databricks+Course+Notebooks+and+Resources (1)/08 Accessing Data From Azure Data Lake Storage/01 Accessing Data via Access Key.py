# Databricks notebook source
# MAGIC %md
# MAGIC # Accessing Data via Access Key
# MAGIC
# MAGIC #### Resources:
# MAGIC * https://learn.microsoft.com/en-us/azure/databricks/external-data/azure-storage#--access-azure-data-lake-storage-gen2-or-blob-storage-using-the-account-key
# MAGIC * https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction-abfs-uri

# COMMAND ----------

# Paste in your account key in the second argument
spark.conf.set(
    "fs.azure.account.key.datalake639.dfs.core.windows.net",
    "PASTE YOUR ACCOUNT KEY HERE")

# COMMAND ----------

# Reading data from the storage account
countries = spark.read.csv("abfss://<YOUR CONTAINER NAME HERE>@<YOUR STORAGE ACCOUNT NAME HERE>.dfs.core.windows.net/countries.csv", header=True)

# COMMAND ----------

# Reading data from the storage account
regions = spark.read.csv("abfss://<YOUR CONTAINER NAME HERE>@<YOUR STORAGE ACCOUNT NAME HERE>.dfs.core.windows.net/country_regions.csv", header=True)

# COMMAND ----------

regions.display()

# COMMAND ----------

countries.display()