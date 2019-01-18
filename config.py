from flask import Flask
from flask_login import LoginManager
import pymysql
import os

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1/livedictdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "random string"

# setting mail server to send stack trace
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER  = os.environ.get('MAIL_DEFAULT_SENDER')

# the address to which the report will be sent
ADMINS = ['alexis.peringer@gmail.com', 'peringer@google.com']  
