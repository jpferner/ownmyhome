from flask_login import UserMixin
from sqlalchemy import PrimaryKeyConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, app


class CalendarEvents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.String(500), nullable=True)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)



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
    email = db.Column(db.String(150), unique=True)  # no user can have an email that's already in db
    password_hash = db.Column(db.String(150))  # hashed password

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

    def get_reset_token(self, expires_secs=300):
        """
        This method creates the token, using itsdangerous, that will verify
        the person and account that will have their password reset
        Args:
            expires_secs: integer number of seconds for expiration

        Returns: a signed string serialized with the internal serializer

        """
        serial = Serializer(app.config['SECRET_KEY'], expires_secs)
        return serial.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)


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
                                   cascade='all, delete-orphan')  # cascade deletes the related UserFavorite instances when a Property is deleted

    def __repr__(self):
        return '<Property {}, {}>'.format(self.propId, self.street)


class UserFavorite(db.Model):
    """ Creates a table and relationship for the favorites list """
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.propId'), primary_key=True)

    user = db.relationship('Users', back_populates='favorite_properties')
    property = db.relationship('Property', back_populates='favorited_by')
