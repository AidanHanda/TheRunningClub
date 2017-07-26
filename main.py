import os

import flask_login
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!


# CONFIG FOR FLASK LOGIN
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"




# ------ END CONFIG FOR FLASK LOGIN -------- #

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.dirname(os.path.abspath(__file__)) + '/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)