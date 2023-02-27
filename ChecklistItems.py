class ChecklistItems:
    def __init__(self, order_no: int, status: str, detail: str):
        self.order_no = order_no
        self.status = status
        self.detail = detail

    def update_status(self, new_status: str):
        self.status = new_status

    def update_detail(self, new_detail: str):
        self.detail = new_detail

    def mark_completed(self):
        self.status = 'Completed'

    @classmethod
    def get_completed(cls, checklists):
        return [c for c in checklists if c.status == 'Completed']

    def __str__(self):
        return f"Step {self.order_no}: {self.detail} ({self.status})"


checklist_items = [ChecklistItems(1, 'Incomplete',
                                  'Do you know what your current credit score is? If not, click here to check it now.'),
                   ChecklistItems(2, 'Incomplete',
                                  'Do you have your home picked out? If not, click here to search for your home.'),
                   ChecklistItems(3, 'Incomplete',
                                  'Do you know what type of financing is available to you? If not,'
                                  'click here to find out your options.')]
