# Databricks notebook source
# MAGIC %md
# MAGIC # Mounting ADLS to DBFS
# MAGIC
# MAGIC #### Resources:
# MAGIC * https://learn.microsoft.com/en-us/azure/databricks/dbfs/mounts

# COMMAND ----------

# syntax for configs and mount methods
configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": "<application-id>",
          "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope="<scope-name>",key="<service-credential-key-name>"),
          "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/<directory-id>/oauth2/token"}

# Optionally, you can add <directory-name> to the source URI of your mount point.
dbutils.fs.mount(
  source = "abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/",
  mount_point = "/mnt/<mount-name>",
  extra_configs = configs)

# COMMAND ----------

# Using dbutils to display mounts
display(dbutils.fs.mounts())

# COMMAND ----------

# Using magic commands
%fs
ls

# COMMAND ----------

# Using dbutils to display directories and files
display(dbutils.fs.ls('/'))

# COMMAND ----------

application_id = "PASTE YOUR APPLICATION ID HERE"

tenant_id = "PASTE YOUR TENANT ID HERE"

secret = "PASTE YOUR SECRET HERE"

# COMMAND ----------

# Performing the mount
configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": "e96a8d39-b788-4e47-9169-db549dca652d",
          "fs.azure.account.oauth2.client.secret": "w2H8Q~CFK_HYwB4MI_sL6gFXjMZ4QhJaEK14AbeD",
          "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/a43c85f4-0351-4195-800b-cea7508b758c/oauth2/token"}

# Optionally, you can add <directory-name> to the source URI of your mount point.
dbutils.fs.mount(
  source = "abfss://<INSERT CONTAINER NAME>@<INSERT STORAGE ACCOUNT NAME>.dfs.core.windows.net/",
  mount_point = "/mnt/bronze",
  extra_configs = configs)

# COMMAND ----------

display(dbutils.fs.mounts())

# COMMAND ----------

# Reading data from the new mount point
spark.read.csv("/mnt/bronze/countries.csv", header=True).display()

# COMMAND ----------

# Using the unmount method to unmount the storage container
dbutils.fs.unmount('/mnt/bronze')