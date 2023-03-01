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
            pass

    @classmethod
    def get_completed(cls, checklists):
        return [c for c in checklists if c.status]

    def __str__(self):
        return f"Step {self.order_no}: {self.detail} ({'Completed' if self.status else 'Incomplete'})"


checklist_items = [ChecklistItems(1, True,
                                  'Do you know what your current credit score is? Check out our services tab above' 
                                  ' to see what options are available to you.'),
                   ChecklistItems(2, True,
                                  'Do you have your home picked out? Check out our properties tab to see what homes' 
                                  ' are available within your search parameters'),
                   ChecklistItems(3, False,
                                  'Do you know what type of financing is available to you?'
                                  ' Check out our services tab above to see what options are available to you.'),
                   ChecklistItems(4, False,
                                  'Do you know how much home you can afford?'
                                  ' Check out our calculator tab to find out the right price for you'),
                   ChecklistItems(5, False,
                                  'Do you understand your current debt to income ratio and what that means,'
                                  ' Check out our calculator tab to find out more.')
                   ]
todo_table = []
completed_table = []
for i in checklist_items:
    if i.status:
        completed_table.append(i)
    else:
        todo_table.append(i)

todo_table = sorted(todo_table, key=lambda x: x.order_no)
completed_table = sorted(completed_table, key=lambda y: y.order_no)