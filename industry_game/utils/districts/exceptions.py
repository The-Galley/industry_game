class DistrictException(Exception):
    pass


class CannotBuildDistrictException(DistrictException):
    def __init__(self, message: str) -> None:
        self.message = message


class CannotProductionDistrictException(DistrictException):
    def __init__(self, message: str) -> None:
        self.message = message
