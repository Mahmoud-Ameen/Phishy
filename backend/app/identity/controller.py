"""
Controllers for identity module handling HTTP requests.
"""
from flask import request
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

from .entity import UserRole
from .service import IdentityService
from app.core.exceptions import UserAlreadyExists, InvalidCredentials
from app.core.middlewares import admin_required
from app.core.response import ApiResponse
from .schemas import UserRegisterSchema, UserResponseSchema, LoginSchema


class IdentityController:
    """Controller handling identity-related HTTP requests."""
    
    @staticmethod
    @admin_required
    def register_user():
        """
        Register a new user (admin only).
        
        Returns:
            Response: JSON response with the new user data or error
        """
        # Validate request data
        try:
            data = UserRegisterSchema().load(request.json)
        except ValidationError as validation_error:
            return ApiResponse.error("Invalid request body", 400, validation_error.messages)

        # Call the service to register the user
        try:
            user = IdentityService.register_user(
                email=data['email'],
                role=UserRole(data['role']),
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password']
            )
        except UserAlreadyExists:
            return ApiResponse.error('A user with this email already exists.')

        return ApiResponse.success(UserResponseSchema().dump(user.to_dict()))
        
    @staticmethod
    def login():
        """
        Authenticate a user and return a JWT token.
        
        Returns:
            Response: JSON response with the JWT token or error
        """
        try:
            # Extract and validate data
            data = request.get_json()
            data = LoginSchema().load(data)

            # Call the service to log the user in
            token = IdentityService.login(data["email"], data["password"])
            return ApiResponse.success(message="Login successful", data={"access_token": token})

        # Handle invalid json
        except (BadRequest, UnsupportedMediaType):
            return ApiResponse.error("Invalid input", 400)

        # Handle invalid input
        except ValidationError as e:
            return ApiResponse.error("Invalid input", 400, details=e.messages)

        # Handle invalid credentials
        except InvalidCredentials:
            return ApiResponse.error("Invalid email or password", 401)
            
    @staticmethod
    @admin_required
    def get_all_users():
        """
        Get all users (admin only).
        
        Returns:
            Response: JSON response with all users data
        """
        users = IdentityService.get_all_users()
        users_data = [user.to_dict() for user in users]
        return ApiResponse.success(data=users_data) 