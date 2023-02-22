class CheckList:
    user_ID: int
    steps: list
    def __int__(self, user: int, steps: list):
        self.user_ID = user
        self.steps = steps


SAMPLE_CHECKLIST = [
    CheckList(111111, ["step 1", "step 2", "step 3"]),
    CheckList(222222, ["step 1", "step 2", "step 3"]),
    CheckList(333333, ["step 1", "step 2", "step 3"])
]
