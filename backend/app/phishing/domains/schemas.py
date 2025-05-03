from marshmallow import Schema, fields, validate


class CreateDomainSchema(Schema):
    domain_name = fields.String(required=True, validate=validate.Regexp(r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'))