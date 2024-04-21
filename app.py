import urllib.parse 
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

params = urllib.parse.quote_plus("")

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
        action = request.form.get('action', '')  # Get the value of 'action' parameter from the form data

        # Sign-in functionality: Check if user exists and password matches
        user = User.query.filter_by(username=username, email=email, password=password).first()
        if user:
            return redirect(url_for('success', message="Sign-in successful!"))
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
        return redirect(url_for('success', message="User registered successfully!"))
    return render_template('register.html')

@app.route('/success')
def success():
    message = request.args.get('message', 'Operation successful!')
    return message

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)
