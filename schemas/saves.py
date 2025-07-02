from marshmallow import Schema, fields

class SavesSchema(Schema):
    id = fields.Str()
    location = fields.Str(required=True)
    party = fields.Int(dump_only=True)