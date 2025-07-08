from marshmallow import Schema, fields

class SaveRequestSchema(Schema):
    location = fields.Str(required=True)

class SaveResponseSchema(Schema):
    id = fields.Str(dump_only=True)
    location = fields.Str(required=True)
    party = fields.List(fields.Str(dump_only=True))
    party_lead = fields.Dict()