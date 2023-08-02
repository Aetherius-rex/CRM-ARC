from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap5
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length
from mongoengine import Document, connect
from urllib.parse import quote_plus
import os, secrets, datetime

DB_URI = "mongodb+srv://"

app = Flask('CRM_DEV')
Bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)
app.secret_key = secrets.token_urlsafe(16)
app.config["MONGODB_SETTINGS"] = [
    {
        "db": "",
        "alias": "",
        "host": "mongodb+srv://",
    }
]

db = MongoEngine(app)

class User(db.Document):
    email = db.StringField(required=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)

class Content(db.EmbeddedDocument):
    text = db.StringField()
    lang = db.StringField(max_length=3)

class Post(db.Document):
    Name = db.StringField(max_length=120, required=True, validators=[DataRequired(message='Missing title.'),Length(5,40)])
    content = db.EmbeddedDocumentField(Content)
    Submit = SubmitField()

PostForm = model_form(Post)

@app.route('/', methods=['GET','POST'])
def add_post():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        # do something
        return("hello")

    return render_template('add_post.html', form=form)
