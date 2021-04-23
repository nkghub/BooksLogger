from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging
db = SQLAlchemy(app)


class user(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), unique=True, nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_reader = db.Column(db.Boolean, default=0)

class book(db.Model):
    bid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    isbn = db.Column(db.String(80), unique=True, nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('User.uid'), nullable=False)
    

class bookread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.bid'), nullable=False)
    stars = db.Column(db.Integer)
    review = db.Column(db.String(120))
