# Databricks notebook source
# MAGIC %md
# MAGIC # Secret Scopes
# MAGIC
# MAGIC #### Resources:
# MAGIC * Secret Scopes: https://learn.microsoft.com/en-us/azure/databricks/security/secrets/secret-scopes
# MAGIC * Secret Management: https://learn.microsoft.com/en-us/azure/databricks/security/secrets/

# COMMAND ----------

# Once you create a key vault, register your secrets and create a secret scope. You can access them via dbutils  
dbutils.secrets.get(scope="YOUR SCOPE HERE", key="YOUR SECRET KEY HERE")

# COMMAND ----------

application_id = dbutils.secrets.get(scope="YOUR SCOPE HERE", key="YOUR SECRET KEY HERE")
tenant_id = dbutils.secrets.get(scope="YOUR SCOPE HERE", key="YOUR SECRET KEY HERE")
secret = dbutils.secrets.get(scope="YOUR SCOPE HERE", key="YOUR SECRET KEY HERE")

# COMMAND ----------

container_name = 'YOUR CONTAINER NAME HERE'
account_name = 'YOUR ACCOUNT NAME HERE'
mount_point = 'YOUR MOUNT POINT PATH HERE'

# COMMAND ----------

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