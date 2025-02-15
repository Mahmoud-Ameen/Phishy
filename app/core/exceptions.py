class AppException(Exception):
    """ Base class for all custom exceptions """
    def __init__(self, message, details=None):
        super().__init__(message)
        self.message = message
        self.details = details

    def to_dict(self):
        return {
            "message": self.message,
            "details": self.details
        }


# region Business Exceptions

class InvalidCredentials(AppException):
    pass


class UserAlreadyExists(AppException):
    pass


class EmployeeAlreadyExists(AppException):
    pass


class DepartmentDoesntExist(AppException):
    pass


class DepartmentAlreadyExists(AppException):
    pass


class TemplateDoesntExist(AppException):
    pass


class EmployeeDoesntExist(AppException):
    pass

# endregion
