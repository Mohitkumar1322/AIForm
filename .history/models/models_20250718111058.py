from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    fields = db.Column(db.Text)  # JSON string of field labels

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'))
    data = db.Column(db.Text)  # JSON string of user responses

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))