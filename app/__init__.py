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
from password_strength import PasswordPolicy

app = Flask(__name__)

# Load configuration from object
app.config.from_object(Config)

# Initialize database
db = SQLAlchemy(app)

# Initialize migration
migrate = Migrate(app, db)

# Set testing mode and secret key
app.config.update(
    TESTING=True,
    SECRET_KEY='8*bb2(n^)jk'
)

# Define password policy
policy = PasswordPolicy.from_names(
    length=8,  # minimum length for password is 8 characters
    uppercase=1,  # requires minimum 1 uppercase letter
    numbers=1,  # requires minimum 1 digit
    strength=0.3  # password score of at least 0.3; good, strong passwords start at 0.66
)

from app import routes, models



if __name__ == '__main__':
    app.run()
