"""
This module contains the main Flask application for the website. It defines the routes and handlers for various pages
of the website, as well as any necessary data processing logic.

It also imports the necessary modules and libraries, including the configuration module, SQLAlchemy for database access,
and data_manager for saving and loading checklist data.

Authors: Mark Karels, David Hollock, Jake Ferner, Connor McNabb, Andrew Court
"""

from flask import Flask, render_template, request, url_for, redirect, jsonify, flash
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

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

from app.models import Users


@login_manager.user_loader
def load_user(user_id):  # id is the primary key for our user in models.py
    return Users.query.get(int(user_id))


from app import routes, models

if __name__ == '__main__':
    app.run()
