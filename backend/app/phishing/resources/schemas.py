from marshmallow import Schema, fields, validate


class CreateResourceSchema(Schema):
    scenario_id = fields.Int(required=True)
    domain_name = fields.String(required=True)
    endpoint = fields.String(required=True, validate=validate.Regexp(r'^[a-zA-Z0-9_\-/]*$'))
    content = fields.String(required=True)
    content_type = fields.String(required=True, validate=validate.OneOf([
        'text/html', 'text/plain', 'application/json', 'image/png', 'image/jpeg', 'image/gif'
    ])) 