import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a2328f7a635e8e74'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'

# initializing modules
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# giving function name of the route, works like 'url_for'
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dori'
app.config['MAIL_PASSWORD'] = '1234'
mail = Mail(app)

from flaskblog import routes
