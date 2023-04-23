from flask_login import UserMixin
from sqlalchemy import PrimaryKeyConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


# Import JWT library for creating and decoding JSON Web Tokens used for authentication
import jwt

from flask import current_app


from app import db, app



class CalendarEvents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.String(500), nullable=True)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class CalculatorUserInputs(db.Model):
    income = db.Column(db.Integer, nullable=False)
    home_val = db.Column(db.Integer)
    down_pay = db.Column(db.Integer)
    loan_amt = db.Column(db.Integer, nullable=False)
    interest_rate = db.Column(db.Numeric(2, 2), nullable=False)
    loan_term = db.Column(db.Integer, nullable=False)
    property_tax = db.Column(db.Integer)
    home_insurance = db.Column(db.Integer)
    monthly_hoa = db.Column(db.Integer)
    pmi = db.Column(db.Numeric(2, 2))
    credit_card_payments = db.Column(db.Integer)
    car_payments = db.Column(db.Integer)
    student_payments = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)


class ChecklistItems(db.Model):
    status = db.Column(db.Boolean, default=False)
    detail = db.Column(db.String(255))
    order_no = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship with the Users table
    user = db.relationship('Users', backref=db.backref('checklist_items', lazy=True))

    __table_args__ = (
        PrimaryKeyConstraint('order_no', 'user_id'),
    )

    def __repr__(self):
        return '<ChecklistItems {}>'.format(self.detail)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True, name='unique_email')  # no user can have an email already in the db
    password_hash = db.Column(db.String(150))  # hashed password
    reset_password_token = db.Column(db.String(150), unique=True, name='unique_reset_password_token')
    reset_password_token_expiration = db.Column(db.DateTime)

    favorite_properties = db.relationship('UserFavorite', back_populates='user')

    # Create a string representation - putting user's first name on screen if desired
    def __repr__(self):
        return '<Name %r>' % self.first_name

    def is_authenticated(self):
        """Return True if user authenticated"""
        return self.is_authenticated()

    # Below is the password hashing for safe storage of passwords in the database
    @property
    def password(self):
        """
        Checks for valid attribute reference
        Returns:
            Invalid attribute error message
        """
        raise AttributeError('Password is not a readable attribute!')

    @password.setter
    def password(self, password):
        """
        Takes the plain text representation of the user's password,
        calls the generate_password_hash method and passes the plain text password
        as an argument, and the newly hashed password is assigned to password_hash
        Args:
            password: string input from user

        Returns:
            Hashed password using hashing algorithm "sha256"
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Takes the users plaintext password and will use it to pass to the check_password_hash function to
        check the user entered password (at login) against the hashed password value stored in the database
        Args:
            password: the plaintext password to compare against the hash.

        Returns:
            True if the password matched, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def generate_password_reset_token(self, expires_in=600):
        now = datetime.utcnow()
        self.reset_password_token = jwt.encode(
            {'reset_password': self.id, 'exp': now + timedelta(seconds=expires_in)},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        self.reset_password_token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit()
        return self.reset_password_token

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
            # user = Users.query.get(id)  #Test triggered deprecation warning
            user = db.session.query(Users).filter_by(id=id).first()
            if not user:
                return None
            # check if the token has expired
            token_exp = user.reset_password_token_expiration
            if datetime.utcnow() > token_exp:
                return None
            return user
        except:
            return None

class Property(db.Model):
    """ Creates the property table and needed relationships"""
    propId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street = db.Column(db.String(100))
    city = db.Column(db.String(25), index=True)
    state = db.Column(db.String(2))
    zcode = db.Column(db.Integer, index=True)
    county = db.Column(db.String(25), index=True)
    price = db.Column(db.Integer)
    yearBuilt = db.Column(db.Integer)
    numBeds = db.Column(db.Integer)
    numBaths = db.Column(db.Integer)
    favorite = db.Column(db.Boolean, default=False)
    image_filename = db.Column(db.String(255))
    propUrl = db.Column(db.String(255), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('properties', lazy=True))
    favorited_by = db.relationship('UserFavorite', back_populates='property', lazy='dynamic',
                                   cascade='all, delete-orphan')

    def __repr__(self):
        return '<Property {}, {}>'.format(self.propId, self.street)


class UserFavorite(db.Model):
    """ Creates a table and relationship for the favorites list """
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.propId'), primary_key=True)

    user = db.relationship('Users', back_populates='favorite_properties')
    property = db.relationship('Property', back_populates='favorited_by')
