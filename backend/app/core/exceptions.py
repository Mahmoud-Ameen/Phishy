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


class DomainAlreadyExists(AppException):
    pass


class ScenarioDoesntExist(AppException):
    pass


class ResourceDoesntExist(AppException):
    pass


class ResourceAlreadyExists(AppException):
    pass


class DomainDoesntExist(AppException):
    pass


class OperationFailure(AppException):
    """ Indicates a general operation failure that might require rollback """
    pass


# endregion
