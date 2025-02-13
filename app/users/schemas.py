from marshmallow import Schema, fields, validate
from .entity import UserRole


class UserRegisterSchema(Schema):
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    role = fields.String(validate=validate.OneOf([role.value for role in UserRole]))


class UserResponseSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    email = fields.Email()
    role = fields.String()
