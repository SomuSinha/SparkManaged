# Databricks notebook source
# MAGIC %md
# MAGIC # Writing to a Data Stream
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
# Please insert your file path
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

#Initialise the stream
orders_sdf.display()

# COMMAND ----------

# Creating a streaming sink
# Please update the filepaths accordingly
streamQuery = orders_sdf.writeStream.format("delta").\
option("checkpointLocation", "/mnt/streaming-demo/streaming_dataset/orders_stream_sink/_checkpointLocation").\
start("/mnt/streaming-demo/streaming_dataset/orders_stream_sink")

# COMMAND ----------

streamQuery.recentProgress

# COMMAND ----------

# reading and displaying the sink dataset as a DataFrame
# Please update the filepaths accordingly
spark.read.format("delta").load("/mnt/streaming-demo/streaming_dataset/orders_stream_sink").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Creating streaming Tables in streaming_db Database

# COMMAND ----------

# MAGIC %sql
# MAGIC create database streaming_db

# COMMAND ----------

# Creating a new streaming query
# the checkpoint location should be different
# This is a managed table, you can also create external tables too
# Please update the filepaths accordingly
streamQuery = orders_sdf.writeStream.format("delta").\
option("checkpointLocation", "/mnt/streaming-demo/streaming_dataset/streaming_db/managed/_checkpointLocation").\
toTable("streaming_db.orders_m")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from streaming_db.orders_m

# COMMAND ----------

# MAGIC %sql
# MAGIC drop table streaming_db.orders_m