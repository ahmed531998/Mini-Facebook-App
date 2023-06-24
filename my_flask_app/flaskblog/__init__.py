from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import flask_whooshalchemy as wa
from flask_whooshalchemyplus import index_all


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ahmed:123456@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['WHOOSH_BASE'] = 'whoosh'
db = SQLAlchemy(app)
index_all(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes
