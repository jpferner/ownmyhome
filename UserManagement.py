class UserManagement:
    """A class representing the User"""
    email: str
    first_name: str
    last_name: str

    def __init__(self, email: str, first_name: str, last_name: str, password: str):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password


# A sample list of users
SAMPLE_USERS = [
    UserManagement("badEmail1@gmail.com", "James", "Green", "password1"),
    UserManagement("badEmail2@hotmail.com", "Kyle", "Brown", "password2"),
    UserManagement("badEmail3@gmail.com", "Sarah", "Smith", "password3"),
    UserManagement("badEmail4@hotmail.com", "Mike", "Jones", "password4")
]
