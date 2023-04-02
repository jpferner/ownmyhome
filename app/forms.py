from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import Regexp

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

    password_hash = PasswordField("Password:",
                                  validators=[InputRequired(),
                                              Length(min=8,
                                                     message='Password should be at least %(min)d characters long'),
                                              Regexp("^(?=.*[A-Z])",
                                                     message="Password must have at least one uppercase character"),
                                              Regexp("^(?=.*[a-z])",
                                                     message="Password must have at least one lowercase character"),
                                              Regexp("^(?=.*\\d)", message="Password must contain at least one number"),
                                              Regexp("(?=.*[@$!%*#?&])",
                                                     message="Password must contain at least one special character"
                                                     ),
                                              ])

    confirm_password_hash = PasswordField("Confirm Password:",
                                          validators=[InputRequired(), EqualTo("password_hash",
                                                                               message="Passwords do not match. "
                                                                                       "Please try "
                                                                                       "again")])

    accept_tos = BooleanField("I accept the Terms of Service.", validators=[InputRequired()])

    create_account = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = StringField("Email:",
                        validators=[InputRequired(), Email(granular_message=True, message="Invalid email format!")])

    # did not set password validators for login page; will flash message if invalid password
    password_hash = PasswordField("Password:", validators=[InputRequired()], id='password_hash')

    # checkbox to show the user's password in plain text
    show_password = BooleanField('Show password', id='check')

    # remember the user once user is signed in; if checked
    remember_me = BooleanField('Remember me', default='checked')

    submit = SubmitField('Submit')

    # IF NEEDED...Custom Form Validation Methods - Will run automatically with WTForms
