import json


class ChecklistItems:
    """
    A class that represents an item in a checklist.

    Attributes:
        button_text (str): The text to display on the button for the item.
        order_no (int): The order number of the item in the checklist.
        status (bool): The completion status of the item.
        detail (str): The details of the item.
    """
    def __init__(self, order_no: int, status: bool, detail: str):
        self.button_text = 'Complete'
        self.order_no = order_no
        self.status = status
        self.detail = detail

    def update_status(self, new_status: bool):
        """
        Updates the completion status of the item.

        Args:
            new_status (bool): The new completion status of the item.
        """
        self.status = new_status

    def update_detail(self, new_detail: str):
        """
        Updates the details of the item.

        Args:
            new_detail (str): The new details of the item.
        """
        self.detail = new_detail

    def toggle_status(self):
        """
        Toggles the completion status of the item and updates the button text.

        This method toggles the completion status of the item and updates the button text
        accordingly. It also saves the updated status to the data file.
        """
        self.status = not self.status
        if self.status:
            self.button_text = 'Undo'
        else:
            self.button_text = 'Complete'
        self.save()  # save the updated status to the checklist_data.json file

    @classmethod
    def from_dict(cls, data):
        """
        Creates a new ChecklistItems object from a dictionary.

        Args:
            data (dict): A dictionary representation of a ChecklistItems object.

        Returns:
            ChecklistItems: A new ChecklistItems object created from the given dictionary.
        """
        return cls(data['order_no'], data['status'], data['detail'])

    def to_dict(self):
        """
        Converts the ChecklistItems object to a dictionary.

        Returns:
            dict: A dictionary representation of the ChecklistItems object.
        """
        return {'order_no': self.order_no, 'status': self.status, 'detail': self.detail}

    @classmethod
    def load(cls):
        """
        Loads a list of ChecklistItems objects from the data file.

        Returns:
            List[ChecklistItems]: A list of ChecklistItems objects loaded from the data file.
        """
        try:
            with open('checklist_data.json', 'r') as f:
                data = json.load(f)
                return [cls.from_dict(item_data) for item_data in data]
        except FileNotFoundError:
            return []

    def save(self):
        """
        Saves the ChecklistItems object to the data file.
        """
        data = self.to_dict()
        with open('checklist_data.json', 'w') as f:
            json.dump(data, f)

    @classmethod
    def update_item(cls, order_no, new_status):
        """
        Updates the completion status of a ChecklistItems object and saves it to the data file.

        Args:
            order_no (int): The order number of the ChecklistItems object to update.
            new_status (bool): The new completion status of the ChecklistItems object.
        """
        checklist_items = cls.load()
        for item in checklist_items:
            if item.order_no == order_no:
                item.status = new_status
                item.toggle_status()
                break
        cls.save_items(checklist_items)

    @classmethod
    def save_items(cls, data):
        """
        Saves a list of ChecklistItems objects to the data file.

        Args:
            data (List[ChecklistItems]): The list of ChecklistItems objects to save to the data file.
        """
        with open('checklist_data.json', 'w') as f:
            json.dump([item.to_dict() for item in data], f)
