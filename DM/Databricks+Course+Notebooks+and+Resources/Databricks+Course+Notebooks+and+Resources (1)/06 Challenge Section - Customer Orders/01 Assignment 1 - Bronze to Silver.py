# Databricks notebook source
# MAGIC %md
# MAGIC # Assignment 1 - Bronze to Silver (Solutions)

# COMMAND ----------

# MAGIC %md
# MAGIC #### ORDERS
# MAGIC
# MAGIC Save a table called ORDERS in the silver layer, it should contain the following columns:
# MAGIC - ORDER_ID, type INTEGER
# MAGIC - ORDER_TIMESTAMP, type TIMESTAMP
# MAGIC - CUSTOMER_ID, type INTEGER
# MAGIC - STORE_NAME, type STRING
# MAGIC
# MAGIC The resulting table should only contain records where the ORDER_STATUS is 'COMPLETE'.
# MAGIC
# MAGIC The file should be saved in PARQUET format.
# MAGIC
# MAGIC Hint 1: You will need to initially read in the ORDER_DATETIME column as a string and then convert it to a timestamp using to_timestamp.
# MAGIC
# MAGIC Hint 2: You will need to merge the orders and stores tables from the bronze layer.
# MAGIC
# MAGIC
# MAGIC ###### Supporting Resources
# MAGIC to_timestamp: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.to_timestamp.html?highlight=to_timestamp#pyspark.sql.functions.to_timestamp
# MAGIC
# MAGIC datetime patterns: https://spark.apache.org/docs/latest/sql-ref-datetime-pattern.html

# COMMAND ----------

# import the relevant data types
from pyspark.sql.types import IntegerType, StringType, DoubleType, StructField, StructType

# COMMAND ----------

# Reading the orders csv file
# Initially assigning the order_datetime column as a string because it is not in the correct timestamp format
# Note in all instances when defining the schema I will set nullable, which is the third argument in StructField to False, this does not permit null values

orders_path = "/FileStore/tables/bronze/orders.csv"

orders_schema = StructType([
                    StructField("ORDER_ID", IntegerType(), False),
                    StructField("ORDER_DATETIME", StringType(), False),
                    StructField("CUSTOMER_ID", IntegerType(), False),
                    StructField("ORDER_STATUS", StringType(), False),
                    StructField("STORE_ID", IntegerType(), False)
                    ]
                    )

orders=spark.read.csv(path=orders_path, header=True, schema=orders_schema)

# COMMAND ----------

# displaying the orders dataframe
orders.display()

# COMMAND ----------

# Importing the to_timestamp function
from pyspark.sql.functions import to_timestamp

# COMMAND ----------

# Converting the order_datetime column to a timestamp and aliasing the name as 'order_timestamp'
# https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.to_timestamp.html?highlight=to_timestamp#pyspark.sql.functions.to_timestamp
# https://spark.apache.org/docs/latest/sql-ref-datetime-pattern.html

orders = orders.select('ORDER_ID', \
              to_timestamp(orders['order_datetime'], "dd-MMM-yy kk.mm.ss.SS").alias('ORDER_TIMESTAMP'), \
              'CUSTOMER_ID', \
              'ORDER_STATUS', \
              'STORE_ID'
             )

# COMMAND ----------

# Confirming the data types
orders.dtypes

# COMMAND ----------

# reviewing the current state of the orders dataframe
orders.display()

# COMMAND ----------

# filtering the records to display only 'COMPLETE' orders
# assigning the result back to the orders dataframe
orders = orders.filter(orders['order_status']=="COMPLETE")

# COMMAND ----------

# Reading the stores csv file

stores_path = "/FileStore/tables/bronze/stores.csv"

stores_schema = StructType([
                    StructField("STORE_ID", IntegerType(), False),
                    StructField("STORE_NAME", StringType(), False),
                    StructField("WEB_ADDRESS", StringType(), False),
                    StructField("LATITUDE", DoubleType(), False),
                    StructField("LONGITUDE", DoubleType(), False)
                    ]
                    )

stores=spark.read.csv(path=stores_path, header=True, schema=stores_schema)

# COMMAND ----------

# displaying the stores dataframe
stores.display()

# COMMAND ----------

# joining the orders and stores via a 'left' join, the orders table is the left table.
# this operation adds the store_name to the orders dataframe
# the final operation is a select method to select only the required columns and assign it back to the orders dataframe

orders = orders.join(stores, orders['store_id']==stores['store_id'], 'left').select('ORDER_ID', 'ORDER_TIMESTAMP', 'CUSTOMER_ID', 'STORE_NAME')

# COMMAND ----------

# the orders dataframe is ready to move to the silver layer
orders.display()

# COMMAND ----------

# writing the orders dataframe as a parquet file in the silver layer, should use mode = 'overwrite' in this instance
orders.write.parquet("/FileStore/tables/silver/orders", mode='overwrite')

# COMMAND ----------

# MAGIC %md
# MAGIC #### ORDER_ITEMS
# MAGIC
# MAGIC Save a table called ORDER_ITEMS in the silver layer, it should contain the following columns:
# MAGIC - ORDER_ID, type INTEGER
# MAGIC - PRODUCT_ID, type INTEGER
# MAGIC - UNIT_PRICE, type DOUBLE
# MAGIC - QUANTITY, type INTEGER
# MAGIC
# MAGIC The file should be saved in PARQUET format.

# COMMAND ----------

# Reading the order items csv file

order_items_path = "/FileStore/tables/bronze/order_items.csv"

order_items_schema = StructType([
                    StructField("ORDER_ID", IntegerType(), False),
                    StructField("LINE_ITEM_ID", IntegerType(), False),
                    StructField("PRODUCT_ID", IntegerType(), False),
                    StructField("UNIT_PRICE", DoubleType(), False),
                    StructField("QUANTITY", IntegerType(), False)
                    ]
                    )

order_items=spark.read.csv(path=order_items_path, header=True, schema=order_items_schema)

# COMMAND ----------

# reviewing the order_items dataframe, the line_item_id column can be removed
order_items.display()

# COMMAND ----------

# selecting only the required columns and assigning this back to the order_items variable
order_items = order_items.drop('LINE_ITEM_ID')

# COMMAND ----------

# revieiwing the order_items dataframe
order_items.display()

# COMMAND ----------

# writing the order_items parquet table in the silver layer
order_items.write.parquet("/FileStore/tables/silver/order_items", mode='overwrite')

# COMMAND ----------

# MAGIC %md
# MAGIC #### PRODUCTS
# MAGIC
# MAGIC Save a table called PRODUCTS in the silver layer, it should contain the following columns:
# MAGIC - PRODUCT_ID, type INTEGER
# MAGIC - PRODUCT_NAME, type STRING
# MAGIC - UNIT_PRICE, type DOUBLE
# MAGIC
# MAGIC The file should be saved in PARQUET format.

# COMMAND ----------

# Reading the products csv file

products_path = "/FileStore/tables/bronze/products.csv"

products_schema = StructType([
                    StructField("PRODUCT_ID", IntegerType(), False),
                    StructField("PRODUCT_NAME", StringType(), False),
                    StructField("UNIT_PRICE", DoubleType(), False)
                    ]
                    )

products=spark.read.csv(path=products_path, header=True, schema=products_schema)

# COMMAND ----------

# reviewing the records
products.display()

# COMMAND ----------

# writing the parquet file
products.write.parquet('/FileStore/tables/silver/products', mode='overwrite')

# COMMAND ----------

# MAGIC %md
# MAGIC #### CUSTOMERS
# MAGIC
# MAGIC Save a table called CUSTOMERS in the silver layer, it should contain the following columns:
# MAGIC - CUSTOMER_ID, type INTEGER
# MAGIC - FULL_NAME, type STRING
# MAGIC - EMAIL_ADDRESS, type STRING
# MAGIC
# MAGIC The file should be saved in PARQUET format.

# COMMAND ----------

# Reading the customers csv file
customers_path = "/FileStore/tables/bronze/customers.csv"

customers_schema = StructType([
                    StructField("CUSTOMER_ID", IntegerType(), False),
                    StructField("FULL_NAME", StringType(), False),
                    StructField("EMAIL_ADDRESS", StringType(), False)
                    ]
                    )

customers=spark.read.csv(path=customers_path, header=True, schema=customers_schema)

# COMMAND ----------

# reviewing the dataframe
customers.display()

# COMMAND ----------

# writing the parquet file
customers.write.parquet('/FileStore/tables/silver/customers', mode='overwrite')