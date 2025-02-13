from flask import request
from marshmallow import ValidationError

from .entity import UserRole
# app specific
from .service import UserService
from ..core.exceptions import UserAlreadyExists
from ..middlewares.auth import admin_required
from ..core.response import ApiResponse
from .schemas import UserRegisterSchema, UserResponseSchema


class UserController:
    @staticmethod
    @admin_required
    def register_user():
        # validate request data
        try:
            data = UserRegisterSchema().load(request.json)  # validate request data
            print('Validated request', data)
        except ValidationError as validation_error:
            return ApiResponse.error("Invalid request body", 400, validation_error.messages)

        # Call the service to register the user
        try:
            user = UserService.register_user(
                email=data['email'],
                role=UserRole(data['role']),
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password']
            )
        # Handle duplicate email error
        except UserAlreadyExists as e:
            return ApiResponse.error('A user with this email already exists.')

        return ApiResponse.success(UserResponseSchema().dump(user.to_dict()))
