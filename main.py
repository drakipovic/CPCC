import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask('triplec', template_folder='templates', static_folder='static')
app.secret_key = 'k)2ehm9j_=ek(9-$h^!5*tumz5yilnmh!=b^=!=8wmy#zu-04m'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

db = SQLAlchemy(app)

from views import *
