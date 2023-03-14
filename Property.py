class Property:
    propnumber: int
    street: str
    city: str
    state: str
    zipcode: int
    county: str
    price: int
    yearBuilt: int
    numBeds: int
    numBaths: int

    def __init__(self, propNumber: int, street: str, city: str, state: str, zipcode: int, county: str, price: int,
                 yearBuilt: int, numBeds: int, numBaths: int, ):
        self.propnumber = propNumber
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.county = county
        self.price = price
        self.yearBuilt = yearBuilt
        self.numBeds = numBeds
        self.numBaths = numBaths


# Sample Property search
SampleProperty = [
    Property(1, "325 Walnut Drive", "Wilmington", "NC", 28409, "New Hanover", 325000, 2018, 3, 2),
    Property(2, "836 Hamilton Road", "Wilmington", "NC", 28412, "New Hanover", 159000, 1996, 2, 2),
    Property(1, "225 Princess Ave", "Wilmington", "NC", 28413, "New Hanover", 825000, 2018, 7, 4),
]
