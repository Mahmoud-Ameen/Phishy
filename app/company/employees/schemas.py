from marshmallow import Schema, fields, validate


class EmployeeCreateSchema(Schema):
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    criticality = fields.Str(required=True, validate=validate.OneOf(['low', 'med', 'high']))
    dept_name = fields.Str(required=True)


class DepartmentCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=255))
