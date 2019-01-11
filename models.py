from config import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    dictionaries = db.relationship('Dictionary', backref='dictionary', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Dictionary(db.Model):
    __tablename__='dictionaries'
    id = db.Column(db.Integer, primary_key=True)
    dict_name = db.Column(db.String(120), index=True, unique=True)
    lang_1 = db.Column(db.String(2))
    lang_2 = db.Column(db.String(2))
    lang_3 = db.Column(db.String(2))
    lang_4 = db.Column(db.String(2))
    lang_5 = db.Column(db.String(2))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Dictionary {}>'.format(self.dict_name)