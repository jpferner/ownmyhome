from app import db


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

    def __repr__(self):
        return '<Property {}, {}>'.format(self.propId, self.street)
