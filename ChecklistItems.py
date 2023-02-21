class ChecklistItems:
    def __init__(self, order_no: int, completed: bool, step_type: str, detail: str):
        self.order_no = order_no
        self.completed = completed
        self.step_type = step_type
        self.detail = detail

    def mark_completed(self):
        self.completed = True

    def update_detail(self, new_detail: str):
        self.detail = new_detail

    @classmethod
    def get_completed(cls, checklists):
        return [c for c in checklists if c.completed]

    def __str__(self):
        return f"Step {self.order_no}: {self.step_type} - {self.detail} " \
               f"({'Completed' if self.completed else 'Incomplete'})"


# Mock data
checklist_item1 = ChecklistItems(1, False, 'Gathering Data',
                                 'Do you know what your current credit score is? If not, click here to check it now.')
checklist_item2 = ChecklistItems(2, False, 'Finding A Home',
                                 'Do you have your home picked out? If not, click here to search for your home.')
checklist_item3 = ChecklistItems(3, False, 'Obtain Financing', 'Do you know what type of financing is available to you?'
                                                               'If not, click here to find out your options.')
