
from typing import List

from app.models import Property


class FavoritesList:

    def __init__(self, favorites: List[Property]):
        self.favorites = favorites

    def add_favorite(self, favorite: Property):
        self.favorites.append(favorite)

    def remove_favorite(self, favorite: Property):
        self.favorites.remove(self.favorites.index(favorite))


sample_property = [
            Property(1, "325 Walnut Drive", "Wilmington", "NC", 28409, "New Hanover", 325000, 2018, 3, 2),
            Property(2, "836 Hamilton Road", "Wilmington", "NC", 28412, "New Hanover", 159000, 1996, 2, 2),
            Property(1, "225 Princess Ave", "Wilmington", "NC", 28413, "New Hanover", 825000, 2018, 7, 4),
        ]

favorites_list = FavoritesList(sample_property)
