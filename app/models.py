from app import db


class Property(db.Model):
    propId = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100))
    city = db.Column(db.String(25), index=True)
    zcode = db.Column(db.Integer, index=True)
    county = db.Column(db.String(25), index=True)
    price = db.Column(db.Integer)
    yearBuilt = db.Column(db.Integer)
    numBeds = db.Column(db.Integer)
    numBaths = db.Column(db.Integer)

    def __repr__(self):
        return '<Property {}, {}>'.format(self.propId, self.street)


class ChecklistItems(db.Model):
    order_no = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    detail = db.Column(db.String(255))

    def __repr__(self):
        return '<ChecklistItems {}>'.format(self.detail)
