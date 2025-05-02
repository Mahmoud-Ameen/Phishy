"""
Schemas for request/response validation in the identity module.
"""
from marshmallow import Schema, fields, validate
from .entity import UserRole


class UserRegisterSchema(Schema):
    """Schema for user registration requests."""
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    role = fields.String(validate=validate.OneOf([role.value for role in UserRole]))


class UserResponseSchema(Schema):
    """Schema for user response data."""
    email = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    role = fields.String()


class LoginSchema(Schema):
    """Schema for login requests."""
    email = fields.Email(required=True)
    password = fields.String(required=True) 