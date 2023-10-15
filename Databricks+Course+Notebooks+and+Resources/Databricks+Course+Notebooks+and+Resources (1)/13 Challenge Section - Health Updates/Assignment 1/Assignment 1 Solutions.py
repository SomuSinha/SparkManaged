# Databricks notebook source
# MAGIC %md
# MAGIC # Assignment 1 - Health Updates (Solutions)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Mounting the health-updates container
# MAGIC #### Change the below scopes, keys, mount points etc. to match your specific settings

# COMMAND ----------

application_id = dbutils.secrets.get(scope = 'databricks-secrets-639', key='application-id')
tenant_id = dbutils.secrets.get(scope = 'databricks-secrets-639', key='tenant-id')
secret = dbutils.secrets.get(scope = 'databricks-secrets-639', key='secret')

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": application_id,
          "fs.azure.account.oauth2.client.secret": secret,
          "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"}

# Optionally, you can add <directory-name> to the source URI of your mount point.
dbutils.fs.mount(
  source = "abfss://health-updates@datalake639.dfs.core.windows.net/",
  mount_point = "/mnt/health-updates",
  extra_configs = configs)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Writing the data to the silver layer

# COMMAND ----------

from pyspark.sql.types import IntegerType, StringType, DoubleType, StructField, StructType

health_data_path = '/mnt/health-updates/bronze/health_status_updates.csv'


health_data_schema = StructType([
                    StructField("STATUS_UPDATE_ID", IntegerType(), False),
                    StructField("PATIENT_ID", IntegerType(), False),
                    StructField("DATE_PROVIDED", StringType(), False),
                    StructField("FEELING_TODAY", StringType(), True),
                    StructField("IMPACT", StringType(), True),
                    StructField("INJECTION_SITE_SYMPTOMS", StringType(), True),
                    StructField("HIGHEST_TEMP", DoubleType(), True),
                    StructField("FEVERISH_TODAY", StringType(), True),
                    StructField("GENERAL_SYMPTOMS", StringType(), True),
                    StructField("HEALTHCARE_VISIT", StringType(), True)
                    ]
                    )

health_data = spark.read.csv(path = health_data_path, header=True, schema=health_data_schema)

# COMMAND ----------

health_data.display()

# COMMAND ----------

from pyspark.sql.functions import to_date, current_timestamp
health_data = health_data.select(
                                'STATUS_UPDATE_ID',
                                'PATIENT_ID',
                                to_date(health_data['DATE_PROVIDED'],'MM/dd/yyyy').alias('DATE_PROVIDED'),
                                'FEELING_TODAY',
                                'IMPACT',
                                'INJECTION_SITE_SYMPTOMS',
                                'HIGHEST_TEMP',
                                'FEVERISH_TODAY',
                                'GENERAL_SYMPTOMS',
                                'HEALTHCARE_VISIT',
                                current_timestamp().alias("UPDATED_TIMESTAMP")
                            )

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating the healthcare database and the health_data external table

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE healthcare

# COMMAND ----------

health_data.write.format("delta").option("path","/mnt/health-updates/silver/health_data").saveAsTable("healthcare.health_data")