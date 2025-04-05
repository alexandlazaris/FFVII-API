from marshmallow import Schema, fields

class CharactersSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)
    weapon = fields.Str(dump_only=True)