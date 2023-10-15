# Databricks notebook source
# MAGIC %md
# MAGIC # Adding New Columns
# MAGIC
# MAGIC #### Resources
# MAGIC * withColumn: https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.DataFrame.withColumn.html?highlight=withcolumn#pyspark.sql.DataFrame.withColumn
# MAGIC * current_date: https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.functions.current_date.html?highlight=current_date
# MAGIC * lit: https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.functions.lit.html

# COMMAND ----------

# Reading in the countries.csv file into a Dataframe called countries
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

# Adding a new column called current_date
from pyspark.sql.functions import current_date
countries.withColumn('current_date', current_date()).display()

# COMMAND ----------

# Adding a new column with a literal value
from pyspark.sql.functions import lit
countries.withColumn('updated_by', lit('MV')).display()

# COMMAND ----------

# Adding a new column derived from using simple arithmetic on an existing column
countries.withColumn('population_m', countries['population']/1000000).display()