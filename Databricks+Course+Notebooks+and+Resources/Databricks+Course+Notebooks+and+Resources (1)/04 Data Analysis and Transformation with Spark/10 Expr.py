# Databricks notebook source
# MAGIC %md
# MAGIC # Expr
# MAGIC
# MAGIC #### Resources:
# MAGIC * https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.expr.html?highlight=expr#pyspark.sql.functions.expr

# COMMAND ----------

# Reading the countries csv file as a Dataframe
countries_path = '/FileStore/tables/countries.csv'
 
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

# Importing the expr function
from pyspark.sql.functions import expr

# COMMAND ----------

countries.display()

# COMMAND ----------

# Expr allows the use of SQL syntax, using the SQL aliasing method
countries.select(expr('NAME as country_name')).display()

# COMMAND ----------

# Expr allows the use of SQL syntax, using the SQL left function
countries.select(expr('left(NAME,2) as name')).display()

# COMMAND ----------

# Expr allows the use of SQL syntax, using the SQL case statement
countries.withColumn('population_class', expr("case when population > 100000000 then 'large' when population >50000000 then 'medium' else 'small' end")).display()

# COMMAND ----------

# Expr allows the use of SQL syntax, using the SQL case statement
countries.withColumn('area_class', expr("case when area_km2 > 1000000 then 'large' when area_km2 > 300000 then 'medium' else 'small' end")).display()