import json
from typing import List
from ChecklistItems import ChecklistItems


class Checklist:
    def __init__(self, name: str, username: str):
        self.name = name
        self.username = username
        self.items = []

    def add_item(self, item: ChecklistItems):
        self.items.append(item)

    def remove_item(self, item: ChecklistItems):
        self.items.remove(item)

    def get_items(self) -> List[ChecklistItems]:
        return self.items

    def to_dict(self):
        return {'name': self.name, 'username': self.username, 'items': [item.to_dict() for item in self.items]}

    @classmethod
    def from_dict(cls, data):
        checklist = cls(data['name'], data['username'])
        items = [ChecklistItems.from_dict(item_data) for item_data in data['items']]
        checklist.items = items
        return checklist

    @classmethod
    def load(cls):
        try:
            with open('checklist_data.json', 'r') as f:
                data = json.load(f)
                return [cls.from_dict(item_data) for item_data in data]
        except FileNotFoundError:
            return []

    def save(self):
        data = self.to_dict()
        with open('checklist_data.json', 'w') as f:
            json.dump(data, f)
