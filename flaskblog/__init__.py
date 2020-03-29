from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


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

from flaskblog import routes
