from marshmallow import Schema, fields, validate


class CreateCampaignSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    employee_emails = fields.List(fields.Str(), required=True)
    template_id = fields.Int(required=True)
