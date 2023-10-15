# Databricks notebook source
# MAGIC %md
# MAGIC # Table Utility Commands
# MAGIC
# MAGIC #### Resources
# MAGIC * https://docs.delta.io/0.4.0/delta-utility.html

# COMMAND ----------

# Describe history can show you the history of operatins performed on a delta lake table

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY '/user/hive/warehouse/delta_lake_db.db/countries_1'

# COMMAND ----------

from delta.tables import *

deltaTable = DeltaTable.forPath(spark, '/user/hive/warehouse/delta_lake_db.db/countries_1')

deltaTable.history().display()

# COMMAND ----------

# You can access previous versions of a table by referencing the version or the timestamp

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM delta_lake_db.countries_1 TIMESTAMP AS OF '2022-11-05T11:20:58.000+0000'

# COMMAND ----------

spark.read.format("delta").option("timestampAsOf", '2022-11-05T11:20:23.000+0000').load("/user/hive/warehouse/delta_lake_db.db/countries_1").display()