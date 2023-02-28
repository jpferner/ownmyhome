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
                                  'Do you know what your current credit score is? Check out our services tab above' 
                                  ' to see what options are available to you.'),
                   ChecklistItems(2, 'Incomplete',
                                  'Do you have your home picked out? Check out our properties tab to see what homes' 
                                  ' are available within your search parameters'),
                   ChecklistItems(3, 'Incomplete',
                                  'Do you know what type of financing is available to you?'
                                  ' Check out our services tab above to see what options are available to you.'),
                   ChecklistItems(4, 'Incomplete',
                                  'Do you know how much home you can afford?'
                                  ' Check out our calculator tab to find out the right price for you'),
                   ChecklistItems(5, 'Incomplete',
                                  'Do you understand your current debt to income ratio and what that means,'
                                  ' Check out our calculator tab to find out more.')
                   ]
sorted_checklist_items = sorted(checklist_items, key=lambda x: x.order_no)
