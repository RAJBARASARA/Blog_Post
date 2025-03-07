from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contacts(db.Model):
    '''sno name email ph_no msg date'''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False) # nullable means this text cannot be empty
    email = db.Column(db.String(100), nullable=False)
    ph_no = db.Column(db.String(15), nullable = False)
    msg = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(12), nullable = True)

class Posts(db.Model):
    '''sno title slug content date'''
    sno = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    img_file = db.Column(db.String(255), nullable=True)

    author = db.relationship('User', backref='posts', lazy=True)  # Define backref only once


class User(db.Model):
    '''id name email password'''
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
