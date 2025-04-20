from marshmallow import Schema, fields, validate


class CreateTemplateSchema(Schema):
    scenario_id = fields.Int(required=True)
    subject = fields.Str(required=True)
    content = fields.Str(required=True)


class CreateScenarioSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True)
    level = fields.Int(required=True)


class UpdateTemplateSchema(Schema):
    subject = fields.Str(required=True)
    content = fields.Str(required=True)


class UpdateScenarioSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True)
    level = fields.Int(required=True, validate=validate.Range(min=1, max=5))

