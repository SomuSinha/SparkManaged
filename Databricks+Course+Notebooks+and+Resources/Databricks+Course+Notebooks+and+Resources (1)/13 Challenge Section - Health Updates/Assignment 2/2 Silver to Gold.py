# Databricks notebook source
# Reading in the silver table into a dataframe
health_data = spark.read.format("delta").load("/mnt/health-updates/silver/health_data")

# COMMAND ----------

# creating the feeling_count_day dataframe
feeling_count_day = health_data.groupBy("date_provided","feeling_today").count()

# COMMAND ----------

# writing the feeling_count_day dataframe as a gold layer table and saving it as an external table
feeling_count_day.write.format("delta").mode("overwrite").option("path","/mnt/health-updates/gold/feeling_count_day").saveAsTable("healthcare.feeling_count_day")

# COMMAND ----------

# creating the symptom_count_day dataframe
symptoms_count_day = health_data.groupBy("date_provided","GENERAL_SYMPTOMS").count()

# COMMAND ----------

# writing the symptom_count_day dataframe as a gold layer table and saving it as an external table
symptoms_count_day.write.format("delta").mode("overwrite").option("path","/mnt/health-updates/gold/symptoms_count_day").saveAsTable("healthcare.symptoms_count_day")

# COMMAND ----------

# creating the healthcare_visit_day dataframe
healthcare_visit_day = health_data.groupBy("date_provided","healthcare_visit").count()

# COMMAND ----------

# writing the healthcare_visit_day dataframe as a gold layer table and saving it as an external table
healthcare_visit_day.write.format("delta").mode("overwrite").option("path","/mnt/health-updates/gold/healthcare_visit_day").saveAsTable("healthcare.healthcare_visit_day")

# COMMAND ----------

dbutils.notebook.exit("Gold Processing Complete")