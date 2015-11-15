import os

# General
basedir = os.path.abspath(os.path.dirname(__file__))

# WTForm
WTF_CSRF_ENABLED = True

# itsdangerous
MAILING_LIST_USER_SALT = 'MAILING_LIST_USER_SALT'
SECRET_KEY = 'dev-key'  # Key will be changed in production

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Mail
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
