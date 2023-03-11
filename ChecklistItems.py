import json


class ChecklistItems:
    def __init__(self, order_no: int, status: bool, detail: str):
        self.button_text = 'Complete'
        self.order_no = order_no
        self.status = status
        self.detail = detail

    def update_status(self, new_status: bool):
        self.status = new_status

    def update_detail(self, new_detail: str):
        self.detail = new_detail

    def toggle_status(self):
        self.status = not self.status
        if self.status:
            self.button_text = 'Undo'
        else:
            self.button_text = 'Complete'
        self.save()  # save the updated status to the checklist_data.json file

    @classmethod
    def from_dict(cls, data):
        return cls(data['order_no'], data['status'], data['detail'])

    def to_dict(self):
        return {'order_no': self.order_no, 'status': self.status, 'detail': self.detail}

    @classmethod
    def load(cls):
        with open('checklist_data.json', 'r') as f:
            data = json.load(f)
        return [cls.from_dict(item_data) for item_data in data]

    def save(self):
        data = self.to_dict()
        with open('checklist_data.json', 'w') as f:
            json.dump(data, f)


checklist_items = ChecklistItems.load()
todo_table = []
completed_table = []
for i in checklist_items:
    if i.status:
        completed_table.append(i)
    else:
        todo_table.append(i)

todo_table = sorted(todo_table, key=lambda x: x.order_no)
completed_table = sorted(completed_table, key=lambda y: y.order_no)
