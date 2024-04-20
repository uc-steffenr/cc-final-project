from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__,
            template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"  # SQLite database
# db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)


# @app.route("/", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         # Create a new user object
#         new_user = User(username=username, password=password)
#         # Add the user to the database
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for("success"))
#     return render_template("register.html")


# @app.route("/success")
# def success():
#     return "User registered successfully!"


# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()  # Create the database tables
#     app.run(debug=True, host="0.0.0.0", port=8080)
