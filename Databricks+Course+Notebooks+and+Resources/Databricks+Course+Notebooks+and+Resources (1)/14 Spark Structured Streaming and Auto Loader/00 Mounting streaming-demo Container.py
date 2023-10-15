# Databricks notebook source
# MAGIC %md
# MAGIC ##### Code to mount the new container to DBFS

# COMMAND ----------

# Mounting the new streaming container into DBFS
application_id = dbutils.secrets.get(scope="YOUR SCOPE HERE", key="YOUR SECRET KEY HERE")
tenant_id = dbutils.secrets.get(scope="YOUR SCOPE HERE", key="YOUR SECRET KEY HERE")
secret = dbutils.secrets.get(scope="YOUR SCOPE HERE", key="YOUR SECRET KEY HERE")

container_name = 'YOUR CONTAINER NAME HERE'
account_name = 'YOUR ACCOUNT NAME HERE'
mount_point = 'YOUR MOUNT POINT PATH HERE'

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