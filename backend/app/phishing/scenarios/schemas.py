from marshmallow import Schema, fields, validate


class CreateTemplateSchema(Schema):
    subject = fields.String(required=True, validate=validate.Length(min=1, max=255))
    content = fields.String(required=True)
    scenario_id = fields.Int(required=True)


class CreateScenarioSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=False)
    level = fields.Int(required=True)

