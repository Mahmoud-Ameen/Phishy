from flask import request
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

from ..core.exceptions import InvalidCredentials
from ..core.response import ApiResponse
from .service import AuthService
from .schemas import LoginSchema


class AuthController:
    @staticmethod
    def login():
        try:
            # Extract and validate data
            data = request.get_json()
            data = LoginSchema().load(data)

            # Call the service to log the user in
            token = AuthService.login(data["email"], data["password"])
            return ApiResponse.success(message="Login successful", data=token)

        # Handle invalid json
        except (BadRequest, UnsupportedMediaType):
            return ApiResponse.error("Invalid input", 400)

        # Handle invalid input
        except ValidationError as e:
            return ApiResponse.error("Invalid input", 400, details=e.messages)

        # Handle invalid credentials
        except InvalidCredentials as e:
            return ApiResponse.error("Invalid email or password", 401)
