class Checklist:
    def __init__(self, name, username):
        self.name = name
        self.username = username
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def get_items(self):
        return self.items
