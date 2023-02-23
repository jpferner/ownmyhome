
from typing import List
import Property


class FavoritesList:

    def __init__(self, favorites: List[Property]):
        self.favorites = favorites

    def add_favorite(self, favorite: Property):
        self.favorites.append(favorite)

    def remove_favorite(self, favorite: Property):
        self.favorites.remove(self.favorites.index(favorite))
