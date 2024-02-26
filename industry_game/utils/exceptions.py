class IndustryGameException(Exception):
    pass


class UserWithUsernameAlreadExistsException(IndustryGameException):
    def __init__(self, username: str) -> None:
        self.username = username

    @property
    def message(self) -> str:
        return f"User with username `{self.username}` already exists"


class UserNotFoundException(IndustryGameException):
    @property
    def message(self) -> str:
        return "User not found"
