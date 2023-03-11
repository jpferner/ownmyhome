import json
from ChecklistItems import ChecklistItems


def save_checklist_data(data):
    with open('checklist_data.json', 'w') as f:
        json.dump([item.to_dict() for item in data], f)


def load_checklist_data():
    try:
        with open('checklist_data.json', 'r') as f:
            data = json.load(f)
            return [ChecklistItems.from_dict(item_data) for item_data in data]
    except FileNotFoundError:
        return []
