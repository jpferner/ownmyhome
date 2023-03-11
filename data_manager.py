import json
from ChecklistItems import ChecklistItems


def save_checklist_data(data):
    with open('checklist_data.json', 'w') as f:
        json.dump([vars(item) for item in data], f)


def load_checklist_data():
    try:
        with open('checklist_data.json', 'r') as f:
            data = json.load(f)
            return [ChecklistItems(item['order_no'], item['status'], item['detail']) for item in data]
    except FileNotFoundError:
        return []
