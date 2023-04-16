"""
This module contains the main Flask application for the website. It defines the routes and handlers for various pages
of the website, as well as any necessary data processing logic.

It also imports the necessary modules and libraries, including the configuration module, SQLAlchemy for database access,
and data_manager for saving and loading checklist data.

Authors: Mark Karels, David Hollock, Jake Ferner, Connor McNabb, Andrew Court
"""
import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail  # for password reset to send the email

from config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# CSRF TOKEN
csrf = CSRFProtect(app)

# Load configuration from object
app.config.from_object(Config)

# Initialize database
db = SQLAlchemy(app)

# Initialize migration
migrate = Migrate(app, db)

# Specify a user loader for Flask-Login
# Used to tell Flask-Login how to find a specific user from the ID stored in their session cookie
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "To access this page, please log into your account."

mail = Mail()
mail.init_app(app)

from app.models import Users


@login_manager.user_loader
def load_user(user_id):  # id is the primary key for our user in models.py
    """
    Fetches a user against the database using user id
    Args:
        user_id: int

    Returns: a new User object

    """
    return Users.query.get(int(user_id))


def create_app(config_class=Config):
    # ...
    if not app.debug and not app.testing:
        # ...

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/microblog.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app


from app import routes, models

if __name__ == '__main__':
    app.run()
