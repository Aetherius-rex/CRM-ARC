from pymongo import MongoClient

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, DateTimeField, PasswordField, validators
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import disconnect
from dotenv import load_dotenv, find_dotenv
import os, secrets, datetime

disconnect()
## Load Authentication Info
load_dotenv(find_dotenv())
username = os.environ.get("MONGODB_USER")
password = os.environ.get("MONGODB_PWD")

## Insert Authentication Info into URI
connection_string = f"mongodb+srv://{username}:{password}@...mongodb.net/WyvernUsers"

## Flask Initialization
db = MongoEngine()
app = Flask("TestApp")
app.secret_key = secrets.token_urlsafe(16)

## Flask-MongoEngine Settings
app.config["MONGODB_SETTINGS"] = [
    {
        "host": connection_string,
        "alias": "Wyvern",
    }
]

## Flask-MongoEngine Init
db.init_app(app)

## Bootstrap and CSRF Init
Bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

class NameForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired(),Length(2,25)])
    user_email = StringField('email:', validators=[DataRequired(),Length(max=60),validators.Email()])
    password = PasswordField('Password:', validators=[DataRequired(),Length(5,60)])
    submit = SubmitField('Submit')

class User(db.Document):
    meta = {
        'db_alias': 'Wyvern',
        'auto_create_index':False,
        }
    username = db.StringField(required=True)
    email = db.EmailField(required=True)
    password_hash = db.StringField(required=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        user_email = form.user_email.data
        password = form.password.data

        if not username or not user_email or not password:
            flash("Please fill in all the fields", "danger")
            return redirect(url_for("index"))
        
        if User.objects(username=name):
            flash("Username already exists. Please choose a different username.", "danger")
            message="User With The Same Name Already Exists. Please Use Another Name."

        if User.objects(email=user_email):
            flash("Email address already exists. Please use a different email.", "danger")
            message="User With The Same Email Already Exists. Please Use Another Email."
        
        user = User(username=name, email=user_email)
        user.set_password(password)
        user.save()
        form.name.data = ""
        form.password.data = ""
        form.user_email.data = ""

    return render_template('form.html', form=form, message=message)