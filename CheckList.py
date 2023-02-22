class CheckList:
    user_ID: int
    steps: list
    user_steps: list
    def __int__(self, user: int, steps: list, user_steps):
        self.user_ID = user
        self.steps = steps
        self.user_steps = user_steps

SAMPLE_CHECKLIST = [
    CheckList(111111, ["step 1", "step 2", "step 3"], [True, True, False]),
    CheckList(222222, ["step 1", "step 2", "step 3"], [True, True, True]),
    CheckList(333333, ["step 1", "step 2", "step 3"], [True, False, False])
]
