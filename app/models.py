from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash





class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)  # no user can have an email that's already in db
    password_hash = db.Column(db.String(150))  # hashed password

    # Create a string representation - putting user's first name on screen if desired
    def __repr__(self):
        return '<Name %r>' % self.first_name

    def is_authenticated(self):
        """Return True if user authenticated"""
        return self.is_authenticated()

    # Below is the password hashing for safe storage of passwords in the database
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password,"sha256")

class Property(db.Model):
    propId = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100))
    city = db.Column(db.String(25), index=True)
    state = db.Column(db.String(2))
    zcode = db.Column(db.Integer, index=True)
    county = db.Column(db.String(25), index=True)
    price = db.Column(db.Integer)
    yearBuilt = db.Column(db.Integer)
    numBeds = db.Column(db.Integer)
    numBaths = db.Column(db.Integer)
    favorite = db.Column(db.Boolean,default=False)
    # not ready yet
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='property_user_id_fk'), nullable=False)
    #user = db.relationship('Users', backref=db.backref('properties', lazy=True))

    def __repr__(self):
        return '<Property {}, {}>'.format(self.propId, self.street)

