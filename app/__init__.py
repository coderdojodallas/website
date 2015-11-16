from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()
mail = Mail()


def create_app(config_filename):
    # Main Flask setup
    app = Flask(__name__)

    # Config setup
    app.config.from_object(config_filename)

    db.init_app(app)
    mail.init_app(app)
    Bootstrap(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
