from flask import Flask
from flask_bootstrap import Bootstrap
# from flask.ext.sqlalchemy import sqlalchemy

app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config')
# db = SQLAlchemy(app)

from app import views
