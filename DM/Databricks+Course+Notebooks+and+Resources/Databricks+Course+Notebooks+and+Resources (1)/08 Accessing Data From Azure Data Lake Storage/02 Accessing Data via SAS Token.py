# Databricks notebook source
# MAGIC %md
# MAGIC # Accessing Data via SAS Token
# MAGIC
# MAGIC #### Resources:
# MAGIC * https://learn.microsoft.com/en-us/azure/databricks/external-data/azure-storage#access-azure-data-lake-storage-gen2-or-blob-storage-using-a-sas-token
# MAGIC * https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction-abfs-uri

# COMMAND ----------

# Setting the configuration
spark.conf.set("fs.azure.account.auth.type.datalake639.dfs.core.windows.net", "SAS")
spark.conf.set("fs.azure.sas.token.provider.type.datalake639.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.sas.FixedSASTokenProvider")
spark.conf.set("fs.azure.sas.fixed.token.datalake639.dfs.core.windows.net", "INSERT SAS TOKEN HERE")

# COMMAND ----------

# Reading data from storage account
spark.read.csv("abfss://<INSERT CONTAINER NAME>@<INSERT STORAGE ACCOUNT NAME>.dfs.core.windows.net/country_regions.csv", header=True).display()