from pyspark.sql import SparkSession
from pyspark.sql.functions import max as spark_max
from pyspark.sql.functions import min as spark_min
from pyspark.sql.functions import col, month, year, avg, expr, collect_list, udf, stddev
from pyspark.sql.types import DoubleType

import pyodbc

# spark = SparkSession.builder \
#     .appName("cc-final-project") \
#     .config("spark.jars", "sqljdbc_12.6/enu/jars/mssql-jdbc-12.6.1.jre8.jar") \
#     .getOrCreate()

connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:cc-final-sql-server.database.windows.net,1433;Database=kroger-data;Uid=final-project;Pwd={CCPaka!@#};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'combined'")
results1 = cursor.fetchall()
cursor.execute("SELECT * FROM combined WHERE HSHD_NUM LIKE '%0010%'")
results = cursor.fetchall()

conn.close()

print(results)