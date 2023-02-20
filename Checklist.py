class Checklist:
    def __init__(self, orderNo: int, completed: bool, stepType: str, detail: str):
        self.orderNo = orderNo
        self.completed = completed
        self.stepType = stepType
        self.detail = detail
    
    def mark_completed(self):
        self.completed = True

    def update_detail(self, new_detail: str):
        self.detail = new_detail

    @classmethod
    def get_completed(cls, checklists):
        return [c for c in checklists if c.completed]

    def __str__(self):
        return f"Step {self.orderNo}: {self.stepType} - {self.detail} ({'Completed' if self.completed else 'Incomplete'})"

# Mock data
checklist1 = Checklist(1, False, 'Gathering Data',
                       'Do you know what your current credit score is? If not, click here to check it now.')
checklist2 = Checklist(2, False, 'Finding A Home',
                       'Do you have your home picked out? If not, click here to search for your home.')
checklist3 = Checklist(3, False, 'Obtain Financing',
                       'Do you know what type of financing is available to you? If not, click here to find out your options.')
