# Databricks notebook source
# MAGIC %md
# MAGIC # Assignment 2 - Silver to Gold (Solutions)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### ORDER_DETAILS
# MAGIC
# MAGIC Create an order_details table that contains the following attributes:
# MAGIC
# MAGIC - ORDER ID
# MAGIC - ORDER DATE
# MAGIC - CUSTOMER ID
# MAGIC - STORE NAME
# MAGIC - TOTAL ORDER AMOUNT 
# MAGIC
# MAGIC The table should be aggregated by ORDER ID, ORDER DATE, CUSTOMER ID and STORE NAME to show the TOTAL ORDER AMOUNT.
# MAGIC
# MAGIC Hint: Please consider the order of operations when finding the TOTAL ORDER AMOUNT.

# COMMAND ----------

# import the functions and read silver data tables as DataFrames
from pyspark.sql.functions import *

orders = spark.read.parquet('/FileStore/tables/silver/orders')
order_items = spark.read.parquet('/FileStore/tables/silver/order_items')
products = spark.read.parquet('/FileStore/tables/silver/products')
customers = spark.read.parquet('/FileStore/tables/silver/customers')

# COMMAND ----------

# display the orders dataframe to review the columns
orders.display()

# COMMAND ----------

# datatype of the order_timestamp column is timestamp and needs to be changed to date
orders.dtypes

# COMMAND ----------

# changing the order_timestamp from 'timestamp' to 'date' using the to_date function
# https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.to_date.html?highlight=to_date#pyspark.sql.functions.to_date
# assigning the result to the order_details dataframe
order_details = orders.select(
'ORDER_ID',
to_date('order_timestamp').alias('DATE'),
'CUSTOMER_ID',
'STORE_NAME'
)

# COMMAND ----------

# reviewing the current state of the order details dataframe
order_details.display()

# COMMAND ----------

# reviewing the columns of the order_items dataframe
order_items.display()

# COMMAND ----------

# joining the order_details and order_items dataframe on the 'order_id' column of both tabes
# selecting the relevant columns from the resulting dataframs and storing it back to the order_details variable
order_details = order_details.join(order_items, order_items['order_id']==order_details['order_id'], 'left'). \
select(order_details['ORDER_ID'], order_details['DATE'], order_details['CUSTOMER_ID'], order_details['STORE_NAME'], order_items['UNIT_PRICE'], order_items['QUANTITY'])

# COMMAND ----------

# reviewing the current state of the order_details dataframe
order_details.display()

# COMMAND ----------

# creating a total amount column at the record level
order_details = order_details.withColumn('TOTAL_SALES_AMOUNT', order_details['UNIT_PRICE']*order_details['QUANTITY'])

# COMMAND ----------

# reviewing the current state of the order_details dataframe
order_details.display()

# COMMAND ----------

# grouping the order_details dataframe and taking the sum of the total amount, renaming this to 'TOTAL_ORDER_AMOUNT'
# assigning the result back to the order_details dataframe
order_details = order_details. \
groupBy('ORDER_ID', 'DATE', 'CUSTOMER_ID', 'STORE_NAME'). \
sum('TOTAL_SALES_AMOUNT'). \
withColumnRenamed('sum(TOTAL_SALES_AMOUNT)', 'TOTAL_ORDER_AMOUNT')

# COMMAND ----------

# reviewing the current state of the order_details dataframe
order_details.display()

# COMMAND ----------

# rounding the TOTAL_ORDER_AMOUNT to 2 dp
order_details = order_details.withColumn('TOTAL_ORDER_AMOUNT', round('TOTAL_ORDER_AMOUNT',2))

# COMMAND ----------

order_details.display()

# COMMAND ----------

# writing the order_details dataframe as a parquet file in the gold layer
order_details.write.parquet('/FileStore/tables/gold/order_details', mode='overwrite')

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### MONTHLY_SALES
# MAGIC
# MAGIC Create an aggregated table to show the monthly sales total and save it in the gold layer as a parquet file called MONTHLY_SALES.
# MAGIC
# MAGIC The table should have two columns:
# MAGIC - MONTH_YEAR - this should be in the format yyyy-MM e.g. 2020-10
# MAGIC - TOTAL_SALES
# MAGIC
# MAGIC Display the sales total rounded to 2 dp and sorted in descending date order.

# COMMAND ----------

# can use the date columns from the order_details table
order_details.display()

# COMMAND ----------

# creating a column that extracts the month and year from the date column
# assigning the dataframe result back to the sales_with_month variable
# https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.date_format.html?highlight=date_format#pyspark.sql.functions.date_format
sales_with_month = order_details.withColumn('MONTH_YEAR', date_format('DATE','yyyy-MM'))

# COMMAND ----------

sales_with_month.display()

# COMMAND ----------

monthly_sales = sales_with_month.groupBy('MONTH_YEAR').sum('TOTAL_ORDER_AMOUNT'). \
withColumn('TOTAL_SALES', round('sum(TOTAL_ORDER_AMOUNT)',2)).sort(sales_with_month['MONTH_YEAR'].desc()). \
select('MONTH_YEAR', 'TOTAL_SALES')

# COMMAND ----------

monthly_sales.display()

# COMMAND ----------

# writing the monthly_sales dataframe as a parquet file in the gold layer
monthly_sales.write.parquet('/FileStore/tables/gold/monthly_sales', mode='overwrite')

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC #### STORE_MONTHLY_SALES
# MAGIC
# MAGIC Create an aggregated table to show the monthly sales total by store and save it in the gold layer as a parquet file called STORE_MONTHLY_SALES.
# MAGIC
# MAGIC The table should have two columns:
# MAGIC - MONTH_YEAR - this should be in the format yyyy-MM e.g. 2020-10
# MAGIC - STORE NAME
# MAGIC - TOTAL_SALES
# MAGIC
# MAGIC Display the sales total rounded to 2 dp and sorted in descending date order.

# COMMAND ----------

# we can leverage the intermediate dataframe called sales_with_month to extract the information we need
sales_with_month.display()

# COMMAND ----------

# in addition to month_year you must also group by store_name
store_monthly_sales = sales_with_month.groupBy('MONTH_YEAR', 'STORE_NAME').sum('TOTAL_ORDER_AMOUNT'). \
withColumn('TOTAL_SALES', round('sum(TOTAL_ORDER_AMOUNT)',2)).sort(sales_with_month['MONTH_YEAR'].desc()). \
select('MONTH_YEAR','STORE_NAME', 'TOTAL_SALES')

# COMMAND ----------

store_monthly_sales.display()

# COMMAND ----------

# writing the store_monthly_sales dataframe as a parquet file in the gold layer
store_monthly_sales.write.parquet('/FileStore/tables/gold/store_monthly_sales', mode='overwrite')

# COMMAND ----------

