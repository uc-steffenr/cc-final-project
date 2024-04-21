from pyspark.sql import SparkSession

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


print(households_df)

products_df = spark.read.format("jdbc") \
    .option("url", "jdbc:sqlserver://cc-final-sql-server.database.windows.net:1433;databaseName=kroger-data") \
    .option("dbtable", "products") \
    .option("user", "final-project") \
    .option("password", "CCPaka!@#") \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .load()


print(products_df)

transactions_df = spark.read.format("jdbc") \
    .option("url", "jdbc:sqlserver://cc-final-sql-server.database.windows.net:1433;databaseName=kroger-data") \
    .option("dbtable", "transactions") \
    .option("user", "final-project") \
    .option("password", "CCPaka!@#") \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .load()


print(transactions_df)

