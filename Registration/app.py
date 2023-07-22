from pymongo import MongoClient

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

app.config['MONGODB_SETTINGS'] = {
    'db': 'dbadmin',
    'host': 'dbadmin.4ebwhy9.mongodb.net',
    'port': 27017,
    'username': 'dbadmin',
    'password': 'db1',
}

db = MongoEngine(app)

class User(db.Document):
    username = db.StringField(unique=True, required=True)
    email = db.EmailField(unique=True, required=True)
    password_hash = db.StringField(required=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route("/")
def hello_world():
    return  """
    <a href="{{ url_for('register') }}">Register</a>
    """

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not username or not email or not password:
            flash("Please fill in all the fields", "danger")
            return redirect(url_for("register"))

        if User.objects(username=username).first():
            flash("Username already exists. Please choose a different username.", "danger")
            return redirect(url_for("register"))

        if User.objects(email=email).first():
            flash("Email address already exists. Please use a different email.", "danger")
            return redirect(url_for("register"))

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")