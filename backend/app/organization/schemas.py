"""
Schemas for request/response validation in the organization module.
"""
from marshmallow import Schema, fields, validate
from .entity import Criticality


class EmployeeCreateSchema(Schema):
    """Schema for employee creation requests."""
    email = fields.Email(required=True)
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    criticality = fields.String(required=True, validate=validate.OneOf([c.value for c in Criticality]))
    dept_name = fields.String(required=True)


class EmployeeUpdateSchema(Schema):
    """Schema for employee update requests."""
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    criticality = fields.String(required=True, validate=validate.OneOf([c.value for c in Criticality]))
    dept_name = fields.String(required=True)


class EmployeeResponseSchema(Schema):
    """Schema for employee response data."""
    email = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    criticality = fields.String()
    dept_name = fields.String()


class DepartmentCreateSchema(Schema):
    """Schema for department creation requests."""
    name = fields.String(required=True, validate=validate.Length(min=1, max=255))


class DepartmentResponseSchema(Schema):
    """Schema for department response data."""
    name = fields.String() 