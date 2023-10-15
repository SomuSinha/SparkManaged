# Databricks notebook source
# Reading in the bronze csv file into a dataframe called health_data 
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

# COMMAND ----------

health_data = spark.read.csv(path = health_data_path, header=True, schema=health_data_schema)

# COMMAND ----------

health_data.display()

# COMMAND ----------

# converting the data type of date_provided
from pyspark.sql.functions import to_date
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
                                'HEALTHCARE_VISIT'
                            )

# COMMAND ----------

# upsert into health_data table
from pyspark.sql.functions import current_timestamp
from delta.tables import *

deltaTable = DeltaTable.forPath(spark, '/mnt/health-updates/silver/health_data')

deltaTable.alias('tgt') \
  .merge(
    health_data.alias('src'),
    'tgt.status_update_id = src.status_update_id'
  ) \
  .whenMatchedUpdate(set =
    {
      "status_update_id": "src.status_update_id",
      "patient_id": "src.patient_id",
      "date_provided": "src.date_provided",
      "feeling_today": "src.feeling_today",
      "impact": "src.impact",
      "injection_site_symptoms": "src.injection_site_symptoms",
      "highest_temp": "src.highest_temp",
      "feverish_today": "src.feverish_today",
      "general_symptoms": "src.general_symptoms",
      "healthcare_visit": "src.healthcare_visit",
      "updated_timestamp": current_timestamp()
    }
  ) \
  .whenNotMatchedInsert(values =
    {
      "status_update_id": "src.status_update_id",
      "patient_id": "src.patient_id",
      "date_provided": "src.date_provided",
      "feeling_today": "src.feeling_today",
      "impact": "src.impact",
      "injection_site_symptoms": "src.injection_site_symptoms",
      "highest_temp": "src.highest_temp",
      "feverish_today": "src.feverish_today",
      "general_symptoms": "src.general_symptoms",
      "healthcare_visit": "src.healthcare_visit",
      "updated_timestamp": current_timestamp()
    }
  ) \
  .execute()

# COMMAND ----------

dbutils.notebook.exit("Silver Processing Complete")