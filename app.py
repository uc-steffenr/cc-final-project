from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
import base64
import io

from pyspark.sql import SparkSession
from pyspark.sql.functions import max as spark_max
from pyspark.sql.functions import min as spark_min
from pyspark.sql.functions import col, month, year, avg, expr, collect_list, udf, stddev
from pyspark.sql.types import DoubleType
import pyodbc

connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:cc-final-sql-server.database.windows.net,1433;Database=kroger-data;Uid=final-project;Pwd={CCPaka!@#};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

# spark = SparkSession.builder \
#     .appName("cc-final-project") \
#     .config("spark.jars", "sqljdbc_12.6/enu/jars/mssql-jdbc-12.6.1.jre8.jar") \
#     .getOrCreate()

# df = spark.read.format("jdbc") \
#     .option("url", "jdbc:sqlserver://cc-final-sql-server.database.windows.net:1433;databaseName=kroger-data") \
#     .option("dbtable", "combined") \
#     .option("user", "final-project") \
#     .option("password", "CCPaka!@#") \
#     .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
#     .load()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def register_or_signin():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Sign-in functionality: Check if user exists and password matches
        user = User.query.filter_by(username=username, email=email, password=password).first()
        if user:
            return redirect(url_for('part_3'))
            # return redirect(url_for('success', message="Sign-in successful!"))
        else:
            return "Invalid username, email, or password. Please try again."

    return render_template('signin_or_register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return "User with this username or email already exists! Please sign in instead."
        # Create a new user
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('part_3'))
        # return redirect(url_for('success', message="User registered successfully!"))
    return render_template('register.html')

@app.route('/success')
def success():
    message = request.args.get('message', 'Operation successful!')
    return message

@app.route('/part_3')
def part_3():
    # rows = df.filter(col('HSHD_NUM').contains('0010')).limit(10).collect()
    # columns = df.columns
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'combined'")
    columns = cursor.fetchall()
    columns = [column[0] for column in columns]
    cursor.execute("SELECT * FROM combined WHERE HSHD_NUM LIKE '%0010%'")
    rows = cursor.fetchall()[:10]
    rows = [list(row) for row in rows]
    conn.close()
    
    return render_template('part_3.html', columns=columns, rows=rows)

@app.route('/part_4', methods=['GET', 'POST'])
def part_4():
    columns = []
    rows = []
    
    if request.method == 'POST':
        lookup_value = request.form['lookup_value']
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'combined'")
        columns = cursor.fetchall()
        columns = [column[0] for column in columns]
        cursor.execute(f"SELECT * FROM combined WHERE HSHD_NUM = {lookup_value}")
        rows = cursor.fetchall()[:10]
        rows = [list(row) for row in rows]
        conn.close()
        
    return render_template('part_4.html', columns=columns, rows=rows)


@app.route('/part_5', methods=['GET', 'POST'])
def part_5():
    # Establish connection to the database
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Execute query to count occurrences of each HH_SIZE value
    cursor.execute("SELECT HH_SIZE, COUNT(*) AS num_transactions FROM combined GROUP BY HH_SIZE ORDER BY HH_SIZE")
    data = cursor.fetchall()

    # Extract HH_SIZE and counts into separate lists
    hh_sizes = [row[0].strip() for row in data]
    print(hh_sizes)
    counts = [row[1] for row in data]

    # Plot bar graph
    pyplot.bar(hh_sizes, counts, color='skyblue')
    pyplot.xlabel('Household Size')
    pyplot.ylabel('Number of Transactions')
    pyplot.title('Number of Transactions by Household Size')
    pyplot.xticks(hh_sizes)  # Set x-ticks to be the household sizes

    # Convert plot to bytes and encode to base64
    buffer = io.BytesIO()
    pyplot.savefig(buffer, format='png')
    buffer.seek(0)
    graph_bytes = base64.b64encode(buffer.getvalue()).decode()
    pyplot.close()
    conn.close()

    return render_template('part_5.html', graph_bytes=graph_bytes)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)
