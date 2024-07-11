class UserCreateException(Exception):
    def __init__(self, message="Failed to create user"):
        self.message = message
        super().__init__(self.message)