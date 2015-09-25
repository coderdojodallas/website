from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager

# Main Flask setup
app = Flask(__name__)

# Email setup
mail = Mail(app)

# Bootstrap setup
Bootstrap(app)

# Config setup
app.config.from_object('config')

# Database and Migrate setup
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app import views, models
