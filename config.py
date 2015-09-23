import os

# General
basedir = os.path.abspath(os.path.dirname(__file__))

# WTForm
WTF_CSRF_ENABLED = True
SECRET_KEY = 'placeholder-key'

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
