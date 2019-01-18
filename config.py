from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
import pymysql
import os

app = Flask(__name__)

app.config.update(
    MAIL_SERVER='smtp.googlemail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=1,
    MAIL_USERNAME = 'alexis.peringer',
    MAIL_PASSWORD = 'Rodion_prod78'
)


mail = Mail(app)
login = LoginManager(app)
login.login_view = 'login'

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1/livedictdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "random string"

# setting mail server to send stack trace
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# the address to which the report will be sent
ADMINS = ['peringer@google.com']  
