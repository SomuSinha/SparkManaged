# Databricks notebook source
# This method can retrieve a parameter from another notebook in a prior task, the task must be called "notebook_01" and the key must be "name"
name  = dbutils.jobs.taskValues.get(taskKey = "notebook_01", key = "name", debugValue = 0)

# COMMAND ----------

print(name)