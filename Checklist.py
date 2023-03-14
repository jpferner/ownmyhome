import json
from typing import List
from ChecklistItems import ChecklistItems


class Checklist:
    """
    A class that represents a checklist.

    Attributes:
        name (str): The name of the checklist.
        username (str): The username of the user who owns the checklist.
        items (List[ChecklistItems]): A list of items in the checklist.
    """
    def __init__(self, name: str, username: str):
        self.name = name
        self.username = username
        self.items = []

    def add_item(self, item: ChecklistItems):
        """
        Adds a new item to the checklist.

        Args:
            item (ChecklistItems): The new item to add to the checklist.
        """
        self.items.append(item)

    def remove_item(self, item: ChecklistItems):
        """
        Removes an item from the checklist.

        Args:
            item (ChecklistItems): The item to remove from the checklist.
        """
        self.items.remove(item)

    def get_items(self) -> List[ChecklistItems]:
        """
        Returns a list of items in the checklist.

        Returns:
            List[ChecklistItems]: A list of items in the checklist.
        """
        return self.items

    def to_dict(self):
        """
        Converts the checklist object to a dictionary.

        Returns:
            dict: A dictionary representation of the checklist object.
        """
        return {'name': self.name, 'username': self.username, 'items': [item.to_dict() for item in self.items]}

    @classmethod
    def from_dict(cls, data):
        """
        Creates a new checklist object from a dictionary.

        Args:
            data (dict): A dictionary representation of a checklist object.

        Returns:
            Checklist: A new checklist object created from the given dictionary.
        """
        checklist = cls(data['name'], data['username'])
        items = [ChecklistItems.from_dict(item_data) for item_data in data['items']]
        checklist.items = items
        return checklist

    @classmethod
    def load(cls):
        """
        Loads a list of checklist objects from the data file.

        Returns:
            List[Checklist]: A list of checklist objects loaded from the data file.
        """
        try:
            with open('checklist_data.json', 'r') as f:
                data = json.load(f)
                return [cls.from_dict(item_data) for item_data in data]
        except FileNotFoundError:
            return []

    def save(self):
        """
        Saves the checklist object to the data file.
        """
        data = self.to_dict()
        with open('checklist_data.json', 'w') as f:
            json.dump(data, f)
