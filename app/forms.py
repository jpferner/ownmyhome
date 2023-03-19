from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired
from wtforms.validators import Email
from wtforms.validators import Length
from wtforms.validators import EqualTo

"""This file is designated to the creation of Forms
    Sign-Up Form and Login Form
"""

class SignUpForm(FlaskForm):
    first_name = StringField("First Name:",
                             validators=[InputRequired(), Length(min=2, max=25, message="First name must be"
                                                                                        "between 2 and 25 characters"
                                                                                        "in length.")])
    last_name = StringField("Last Name:",
                            validators=[InputRequired(), Length(min=2, max=25, message="First name must be"
                                                                                       "between 2 and 25 characters"
                                                                                       "in length.")])
    email = StringField("Email:",
                        validators=[InputRequired(), Email(granular_message=True)])

    confirm_email = StringField("Confirm Email:",
                                validators=[InputRequired(), EqualTo("email", message='Emails do not match. Please '
                                                                                      'try again.')])

    password = PasswordField("Password:",
                             validators=[InputRequired(),
                                         Length(min=8, message='Password should be at least %(min)d characters long')])

    confirm_password = PasswordField("Confirm Password:",
                                     validators=[InputRequired(), EqualTo("password",
                                                                          message="Passwords do not match. Please try "
                                                                                  "again")])

    accept_tos = BooleanField("I accept the Terms of Service.", validators=[InputRequired()])

    create_account = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = StringField("Email:",
                        validators=[InputRequired(), Email(granular_message=True)])

    # did not set password validators for login page; will flash message if invalid password
    password = PasswordField("Password:", validators=[InputRequired()])

    submit = SubmitField('Submit')

    # IF NEEDED...Custom Form Validation Methods - Will run automatically with WTForms
