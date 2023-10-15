# Databricks notebook source
# MAGIC %md
# MAGIC # End to end demo
# MAGIC
# MAGIC #### The code in this section is unchanged, it is for your reference only. You will need to register your own secrets and update the arguments to be able to successfully execute this notebook.

# COMMAND ----------

application_id = dbutils.secrets.get(scope="databricks-secrets-639",key="application-id")
tenant_id = dbutils.secrets.get(scope="databricks-secrets-639",key="tenant-id")
secret = dbutils.secrets.get(scope="databricks-secrets-639",key="secret")

# COMMAND ----------

container_name = "gold"
account_name = "datalake639"
mount_point = "/mnt/gold"

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": application_id,
          "fs.azure.account.oauth2.client.secret": secret,
          "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"}
 
dbutils.fs.mount(
  source = f"abfss://{container_name}@{account_name}.dfs.core.windows.net/",
  mount_point = mount_point,
  extra_configs = configs)

# COMMAND ----------

countries_path = '/mnt/bronze/countries.csv'
 
from pyspark.sql.types import IntegerType, StringType, DoubleType, StructField, StructType
countries_schema = StructType([
                    StructField("COUNTRY_ID", IntegerType(), False),
                    StructField("NAME", StringType(), False),
                    StructField("NATIONALITY", StringType(), False),
                    StructField("COUNTRY_CODE", StringType(), False),
                    StructField("ISO_ALPHA2", StringType(), False),
                    StructField("CAPITAL", StringType(), False),
                    StructField("POPULATION", DoubleType(), False),
                    StructField("AREA_KM2", IntegerType(), False),
                    StructField("REGION_ID", IntegerType(), True),
                    StructField("SUB_REGION_ID", IntegerType(), True),
                    StructField("INTERMEDIATE_REGION_ID", IntegerType(), True),
                    StructField("ORGANIZATION_REGION_ID", IntegerType(), True)
                    ]
                    )
 
countries=spark.read.csv(path=countries_path, header=True, schema=countries_schema)

# COMMAND ----------

countries.display()

# COMMAND ----------

countries = countries.drop("sub_region_id","intermediate_region_id","organization_region_id")

# COMMAND ----------

countries.display()

# COMMAND ----------

countries.write.parquet('/mnt/silver/countries')

# COMMAND ----------

regions_path = '/mnt/bronze/country_regions.csv'
 
regions_schema = StructType([
                    StructField("Id", StringType(), False),
                    StructField("NAME", StringType(), False)
                    ]
                    )
 
regions = spark.read.csv(path=regions_path, header=True, schema=regions_schema)

# COMMAND ----------

regions.display()

# COMMAND ----------

regions = regions.withColumnRenamed('NAME','REGION_NAME')

# COMMAND ----------

regions.display()

# COMMAND ----------

regions.write.parquet('/mnt/silver/regions')

# COMMAND ----------

countries = spark.read.parquet('/mnt/silver/countries')
regions = spark.read.parquet('/mnt/silver/regions')

# COMMAND ----------

countries.display()

# COMMAND ----------

regions.display()

# COMMAND ----------

country_data = countries.join(regions, countries['region_id']==regions['Id'], 'left').drop('Id','region_id','country_code', 'iso_alpha_2')

# COMMAND ----------

country_data.display()

# COMMAND ----------

country_data.write.parquet('/mnt/gold/country_data')