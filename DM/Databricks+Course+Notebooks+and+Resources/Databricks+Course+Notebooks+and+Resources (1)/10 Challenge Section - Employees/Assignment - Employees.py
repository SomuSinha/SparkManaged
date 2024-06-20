# Databricks notebook source
# MAGIC %md
# MAGIC # Assignment 2 - Employees (Solutions)

# COMMAND ----------

# MAGIC %md
# MAGIC #### 1. Mount the employees container to DBFS
# MAGIC
# MAGIC https://docs.databricks.com/dbfs/mounts.html

# COMMAND ----------

# insert your scope and key in the secrets.get method
# ensure you have set up the secret scopes and stored your IDs and keys in the key vault
application_id = dbutils.secrets.get(scope='INSERT SCOPE HERE', key = 'INSERT APP ID HERE')
tenant_id = dbutils.secrets.get(scope='INSERT SCOPE HERE', key = 'INSERT TENANT ID HERE')
secret = dbutils.secrets.get(scope='INSERT SCOPE HERE', key = 'INSERT SECRET HERE')

# COMMAND ----------

 # Ensure your secret is still valid, if it has expired you will have to re-generate the secret and store it in the key vault

configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": application_id,
          "fs.azure.account.oauth2.client.secret": secret,
          "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"}

# Optionally, you can add <directory-name> to the source URI of your mount point.
dbutils.fs.mount(
  source = "abfss://employees@datalake639.dfs.core.windows.net/",
  mount_point = "/mnt/employees",
  extra_configs = configs)

# COMMAND ----------

# MAGIC %md
# MAGIC #### 2. Adding parquet files to the silver folder of the employees container

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Employees

# COMMAND ----------

# Importing the data types
from pyspark.sql.types import IntegerType, StringType, DoubleType, StructField, StructType, DateType

# COMMAND ----------

# Reading in the employees csv file from the bronze layer
# Reading in the hire_date as a string to avoid formatting issues during the read operation
employees_path = '/mnt/employees/bronze/employees.csv'
 

employees_schema = StructType([
                    StructField("EMPLOYEE_ID", IntegerType(), False),
                    StructField("FIRST_NAME", StringType(), False),
                    StructField("LAST_NAME", StringType(), False),
                    StructField("EMAIL", StringType(), False),
                    StructField("PHONE_NUMBER", StringType(), False),
                    StructField("HIRE_DATE", StringType(), False),
                    StructField("JOB_ID", StringType(), False),
                    StructField("SALARY", IntegerType(), False),
                    StructField("MANAGER_ID", IntegerType(), True),
                    StructField("DEPARTMENT_ID", IntegerType(), False)
                    ]
                    )
 
employees=spark.read.csv(path=employees_path, header=True, schema=employees_schema)

# COMMAND ----------

employees.display()

# COMMAND ----------

# Dropping unnecessary columns
employees = employees.drop("EMAIL", "PHONE_NUMBER")

# COMMAND ----------

employees.display()

# COMMAND ----------

# Changing the data type of hire_date from string to data via the to_date function
# https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.to_date.html?highlight=to_date#pyspark.sql.functions.to_date
# https://spark.apache.org/docs/latest/sql-ref-datetime-pattern.html
from pyspark.sql.functions import to_date
employees = employees.select(
    "EMPLOYEE_ID",
    "FIRST_NAME",
    "LAST_NAME",
    to_date(employees["HIRE_DATE"], "MM/dd/yyyy").alias('HIRE_DATE'),
    "JOB_ID",
    "SALARY",
    "MANAGER_ID",
    "DEPARTMENT_ID"
)

# COMMAND ----------

employees.display()

# COMMAND ----------

# Writing dataframe as parquet file to the silver layer
employees.write.parquet("/mnt/employees/silver/employees", mode='overwrite')

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Departments

# COMMAND ----------

# Reading in the departments csv file from the bronze layer
dept_path = '/mnt/employees/bronze/departments.csv'
 

dept_schema = StructType([
                    StructField("DEPARTMENT_ID", IntegerType(), False),
                    StructField("DEPARTMENT_NAME", StringType(), False),
                    StructField("MANAGER_ID", IntegerType(), True),
                    StructField("LOCATION_ID", IntegerType(), False)
                    ]
                    )
 
dept=spark.read.csv(path=dept_path, header=True, schema=dept_schema)

# COMMAND ----------

dept.display()

# COMMAND ----------

# Dropping unnecessary columns
dept = dept.drop("MANAGER_ID", "LOCATION_ID")

# COMMAND ----------

# Writing dataframe as parquet file to the silver layer
dept.write.parquet("/mnt/employees/silver/departments", mode='overwrite')

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Countries

# COMMAND ----------

# Reading in the countries csv file from the bronze layer
countries_path = '/mnt/employees/bronze/countries.csv'
 

countries_schema = StructType([
                    StructField("COUNTRY_ID", StringType(), False),
                    StructField("COUNTRY_NAME", StringType(), False)
                    ]
                    )
 
countries=spark.read.csv(path=countries_path, header=True, schema=countries_schema)

# COMMAND ----------

countries.display()

# COMMAND ----------

# Writing dataframe as parquet file to the silver layer
countries.write.parquet("/mnt/employees/silver/countries", mode='overwrite')

# COMMAND ----------

# MAGIC %md
# MAGIC #### 3. Adding parquet files to the gold folder of the employees container

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Employees

# COMMAND ----------

employees = spark.read.parquet("/mnt/employees/silver/employees")

# COMMAND ----------

employees.display()

# COMMAND ----------

# create a new column called full_name via the withColumn method and using the concat_ws function
from pyspark.sql.functions import concat_ws
employees=employees.withColumn("FULL_NAME", concat_ws(' ', employees['FIRST_NAME'], employees['LAST_NAME']))

# COMMAND ----------

employees.display()

# COMMAND ----------

# Dropping unnecessary columns
employees = employees.drop("FIRST_NAME", "LAST_NAME", "MANAGER_ID")

# COMMAND ----------

employees.display()

# COMMAND ----------

# Reading in the departments parquet file from the silver layer
departments = spark.read.parquet("/mnt/employees/silver/departments")

# COMMAND ----------

departments.display()

# COMMAND ----------

# Joining the employees and departments silver tables to include the relevant fields such as department id, and drop columns that are not required
employees = employees.join(departments, employees['department_id']==departments['department_id'], 'left').select("EMPLOYEE_ID", "FULL_NAME","HIRE_DATE", "JOB_ID", "SALARY", "DEPARTMENT_NAME")

# COMMAND ----------

employees.display()

# COMMAND ----------

# Writing the employees dataframe to the gold layer
employees.write.parquet("/mnt/employees/gold/employees")

# COMMAND ----------

# MAGIC %md
# MAGIC #### Creating the employees database and loading the gold layer table

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS employees;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE employees.employees 
# MAGIC (
# MAGIC   EMPLOYEE_ID int,
# MAGIC   FULL_NAME string,
# MAGIC   HIRE_DATE date, 
# MAGIC   JOB_ID string,
# MAGIC   SALARY int,
# MAGIC   DEPARTMENT_NAME string
# MAGIC   )
# MAGIC USING parquet
# MAGIC LOCATION '/mnt/employees/gold/employees'
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM employees.employees;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC DESCRIBE EXTENDED employees.employees