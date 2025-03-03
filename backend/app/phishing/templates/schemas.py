from marshmallow import Schema, fields, validate


class CreateTemplateSchema(Schema):
    subject = fields.String(required=True, validate=validate.Length(min=1, max=255))
    content = fields.String(required=True)
    level = fields.Int(required=True, validate=validate.Range(min=1, max=5))

