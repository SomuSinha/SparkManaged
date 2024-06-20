# Databricks notebook source
# MAGIC %md
# MAGIC # Reading a Data Stream
# MAGIC
# MAGIC #### Resources:
# MAGIC * Structured Streaming API: https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/index.html
# MAGIC * DataStreamReader API: https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/api/pyspark.sql.streaming.DataStreamReader.html
# MAGIC * DataStreamWriter API: https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/api/pyspark.sql.streaming.DataStreamWriter.html
# MAGIC * Input / Output: https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/io.html
# MAGIC * Query Management: https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/query_management.html

# COMMAND ----------

# import the relevant data types
from pyspark.sql.types import IntegerType, StringType, DoubleType, StructField, StructType

# For a streaming source DataFrame we must define the schema
# Please update with your specific file path and assign it to the variable orders_full_path
orders_streaming_path = "/mnt/streaming-demo/streaming_dataset/orders_streaming.csv"
 
orders_schema = StructType([
                    StructField("ORDER_ID", IntegerType(), False),
                    StructField("ORDER_DATETIME", StringType(), False),
                    StructField("CUSTOMER_ID", IntegerType(), False),
                    StructField("ORDER_STATUS", StringType(), False),
                    StructField("STORE_ID", IntegerType(), False)
                    ]
                    )

# COMMAND ----------

# reading the streaming data into a dataframe called orders_sdf
orders_sdf = spark.readStream.csv(orders_streaming_path, orders_schema, header=True )

# COMMAND ----------

# displaying the dataframe initialises the stream
orders_sdf.display()