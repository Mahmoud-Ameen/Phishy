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
class BusinessException(AppException):
    pass


class InvalidCredentials(BusinessException):
    pass


class UserAlreadyExists(BusinessException):
    pass

# endregion

# region Repository Exceptions
class RepositoryException(AppException):
    pass

# endregion
