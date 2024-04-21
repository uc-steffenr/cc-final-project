from pyspark.sql import SparkSession
from pyspark.sql.functions import max as spark_max
from pyspark.sql.functions import min as spark_min
from pyspark.sql.functions import col, month, year, avg, expr, collect_list, udf, stddev
from pyspark.sql.types import DoubleType

spark = SparkSession.builder \
    .appName("cc-final-project") \
    .config("spark.jars", "sqljdbc_12.6/enu/jars/mssql-jdbc-12.6.1.jre8.jar") \
    .getOrCreate()

households_df = spark.read.format("jdbc") \
    .option("url", "jdbc:sqlserver://cc-final-sql-server.database.windows.net:1433;databaseName=kroger-data") \
    .option("dbtable", "households") \
    .option("user", "final-project") \
    .option("password", "CCPaka!@#") \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .load()


# print(households_df)

products_df = spark.read.format("jdbc") \
    .option("url", "jdbc:sqlserver://cc-final-sql-server.database.windows.net:1433;databaseName=kroger-data") \
    .option("dbtable", "products") \
    .option("user", "final-project") \
    .option("password", "CCPaka!@#") \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .load()


# print(products_df)

transactions_df = spark.read.format("jdbc") \
    .option("url", "jdbc:sqlserver://cc-final-sql-server.database.windows.net:1433;databaseName=kroger-data") \
    .option("dbtable", "transactions") \
    .option("user", "final-project") \
    .option("password", "CCPaka!@#") \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .load()


# print(transactions_df)


# df = households_df.join(products_df.join(transactions_df))

# df.filter('HSHD_NUM')

df = transactions_df.join(products_df, 'PRODUCT_NUM', 'inner')

df.show()