# Databricks notebook source
# MAGIC %md
# MAGIC # Merge Into
# MAGIC
# MAGIC #### Resources
# MAGIC * https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/delta-merge-into
# MAGIC * https://docs.delta.io/latest/delta-update.html
# MAGIC * https://docs.delta.io/0.4.0/delta-update.html

# COMMAND ----------

# Reading in the countries csv file from the bronze container
countries = spark.read.csv('/mnt/bronze/countries.csv', header=True, inferSchema=True)

# COMMAND ----------

countries.display()

# COMMAND ----------

# Creating a subset of countries called countries_1
countries_1 = countries.filter("region_id in (10,20,30)")

# COMMAND ----------

countries_1.display()

# COMMAND ----------

# Creating a subset of countries called countries_2
countries_2 = countries.filter("region_id in (20,30,40,50)")

# COMMAND ----------

countries_2.display()

# COMMAND ----------

# creating a delta table
countries_1.write.format("delta").saveAsTable("delta_lake_db.countries_1")

# COMMAND ----------

# creating a delta table
countries_2.write.saveAsTable("delta_lake_db.countries_2")

# COMMAND ----------

# Updating countries_2 to have upper case name column values

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE delta_lake_db.countries_2
# MAGIC SET name = upper(name)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM delta_lake_db.countries_1

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM delta_lake_db.countries_2

# COMMAND ----------

# Below I am merging countries_1 and countries_2 using SQL syntax
# countries_1 is the target and countries_2 is the source. The merge is happening by referencing the country_id columns
# When matched only the name column is updates
# When not matched then all columns are inserted from the source to the target

# COMMAND ----------

# MAGIC %sql
# MAGIC  
# MAGIC MERGE INTO delta_lake_db.countries_1 tgt
# MAGIC USING delta_lake_db.countries_2 src
# MAGIC ON tgt.country_id = src.country_id
# MAGIC WHEN MATCHED THEN
# MAGIC   UPDATE SET
# MAGIC     tgt.name = src.name
# MAGIC WHEN NOT MATCHED
# MAGIC   THEN INSERT (
# MAGIC     tgt.country_id,
# MAGIC     tgt.name,
# MAGIC     tgt.nationality,
# MAGIC     tgt.country_code,
# MAGIC     tgt.iso_alpha2,
# MAGIC     tgt.capital,
# MAGIC     tgt.population,
# MAGIC     tgt.area_km2,
# MAGIC     tgt.region_id,
# MAGIC     tgt.sub_region_id,
# MAGIC     tgt.intermediate_region_id,
# MAGIC     tgt.organization_region_id
# MAGIC   )
# MAGIC   VALUES (
# MAGIC     src.country_id,
# MAGIC     src.name,
# MAGIC     upper(src.nationality),
# MAGIC     src.country_code,
# MAGIC     src.iso_alpha2,
# MAGIC     src.capital,
# MAGIC     src.population,
# MAGIC     src.area_km2,
# MAGIC     src.region_id,
# MAGIC     src.sub_region_id,
# MAGIC     src.intermediate_region_id,
# MAGIC     src.organization_region_id
# MAGIC   )

# COMMAND ----------

# Below I am merging countries_1 and countries_2 using Python syntax
# countries_1 is the target and countries_2 is the source. The merge is happening by referencing the country_id columns
# When matched only the name column is updates
# When not matched then all columns are inserted from the source to the target

# COMMAND ----------

from delta.tables import *
from pyspark.sql.functions import *
 
deltaTable = DeltaTable.forPath(spark, "/user/hive/warehouse/delta_lake_db.db/countries_1")

# COMMAND ----------

deltaTable.alias("target").merge(
    countries_2.alias("source"),
    "target.country_id = source.country_id") \
  .whenMatchedUpdate(set = { 
      "name": "source.name"
} ) \
  .whenNotMatchedInsert(values =
    {
      "country_id": "source.country_id",
      "name": "source.name",
      "nationality": "source.nationality",
      "country_code": "source.country_code",
      "iso_alpha2": "source.iso_alpha2",
      "capital": "source.capital",
      "population": "source.population",
      "area_km2": "source.area_km2",
      "region_id": "source.region_id",
      "sub_region_id": "source.sub_region_id",
      "intermediate_region_id": "source.intermediate_region_id",
      "organization_region_id": "source.organization_region_id"
    }
  ) \
  .execute()