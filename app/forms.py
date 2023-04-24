from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import Regexp

from flask import Markup

"""This file is designated to the creation of Forms
    Sign-Up Form and Login Form
"""


class SignUpForm(FlaskForm):
    # first_name = StringField("First Name:", render_kw={"placeholder": "First name"},
    #                          validators=[InputRequired(), Length(min=2, max=25, message="First name must be"
    #                                                                                     "between 2 and 25 characters"
    #                                                                                     "in length."),
    #                                      Regexp("^[^\s\[\.<>/\\\\]*$",
    #                                             message="Invalid character in first name."), ])
    first_name = StringField("First Name:", render_kw={"placeholder": "First name"},
                             validators=[InputRequired(),
                                         Length(min=2, max=25,
                                                message="First name must be between 2 and 25 characters in length."),
                                         Regexp("^[A-Za-z'-]+$", message="Invalid character in first name."), ])

    last_name = StringField("Last Name:", render_kw={"placeholder": "Last name"},
                            validators=[InputRequired(),
                                        Length(min=2, max=25,
                                               message="Last name must be between 2 and 25 characters in length."),
                                        Regexp("^[A-Za-z'-]+$", message="Invalid character in last name."), ])
    email = StringField("Email:", render_kw={"placeholder": "Email"},
                        validators=[InputRequired(), Email('Valid email address required.'),
                                    Regexp("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$",
                                           message="Invalid or missing character(s) in email address.")
                                    ])

    confirm_email = StringField("Confirm Email:", render_kw={"placeholder": "Confirm email"},
                                validators=[InputRequired(), EqualTo("email", message='Emails do not match. Please '
                                                                                      'try again.')])

    password_hash = PasswordField("Password:", render_kw={"placeholder": "Password"},
                                  validators=[InputRequired(),
                                              Length(min=8,
                                                     message='Password should be at least %(min)d characters long'),
                                              Regexp(
                                                  r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\w\s])[^\s<>./\\#$]*$',
                                                  message="Password must have at least one uppercase character, \n"
                                                          "at least one lowercase character, \nat least one number,\n "
                                                          "and at least one special character.")
                                              ], id='password_hash')
    r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\w\s]).{8,}$"

    # checkbox to show the user's password in plain text
    show_password = BooleanField('Show password', id='check')

    confirm_password_hash = PasswordField("Confirm Password:", render_kw={"placeholder": "Confirm password"},
                                          validators=[InputRequired(), EqualTo("password_hash",
                                                                               message="Passwords do not match. "
                                                                                       "Please try "
                                                                                       "again")],
                                          id='confirm_password_hash')

    # checkbox to show the user's password in plain text
    confirm_show_password = BooleanField('Show password', id='confirm_check')

    # url label for Terms of Service
    url_label = Markup(
        "<a id='tos' target='_blank' href='https://www.termsandconditionsgenerator.com/live.php?token"
        "=WHZDugV9ku8Yfxs8mVwMZIhx12VmZHpr'>Terms of Service.</a>")

    accept_tos = BooleanField("I accept the " + url_label, validators=[InputRequired()])

    create_account = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = StringField("Email:", render_kw={"placeholder": "Email"},
                        validators=[InputRequired(), Email('Valid email address required.'),
                                    Regexp("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$",
                                           message="Invalid or missing character(s) in email address.")
                                    ])

    # did not set password validators for login page; will flash message if invalid password
    password_hash = PasswordField("Password:", render_kw={"placeholder": "Password"},
                                  validators=[InputRequired(),
                                              Regexp(r"^[^\s\[\.<>/\\\\]*$",
                                                     message="Password cannot contain ., <, >, /, \\, "
                                                             "or spaces.")], id='password_hash')

    # checkbox to show the user's password in plain text
    show_password = BooleanField('Show password', id='check')

    # remember the user once user is signed in; if checked
    remember_me = BooleanField('Remember me', default='checked')

    submit = SubmitField('Submit')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email:", render_kw={"placeholder": "Email"},
                        validators=[InputRequired(), Email('Valid email address required.'),
                                    Regexp("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$",
                                           message="Invalid or missing character(s) in email address.")
                                    ])

    submit = SubmitField('Reset Password')


class ResetPasswordForm(FlaskForm):
    password_hash = PasswordField("New Password:", render_kw={"placeholder": "new password"},
                                  validators=[InputRequired(),
                                              Length(min=8,
                                                     message='Password should be at least %(min)d characters long'),
                                              Regexp(
                                                  r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\w\s])[^\s<>./\\#$]*$',
                                                  message="Password must have at least one uppercase character, \n"
                                                          "at least one lowercase character, \nat least one number,\n "
                                                          "and at least one special character.")
                                              ], id='password_hash')

    # checkbox to show the user's password in plain text
    show_password = BooleanField('Show password', id='check')

    confirm_password_hash = PasswordField("Confirm New Password:", render_kw={"placeholder": "confirm password"},
                                          validators=[InputRequired(), EqualTo("password_hash",
                                                                               message="Passwords do not match. "
                                                                                       "Please try "
                                                                                       "again.")],
                                          id='confirm_password_hash')

    # checkbox to show the user's password in plain text
    confirm_show_password = BooleanField('Show password', id='confirm_check')

    submit = SubmitField('Change Password')
