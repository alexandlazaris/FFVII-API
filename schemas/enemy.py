from marshmallow import Schema, fields

class EnemySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    hp = fields.Int()
    description = fields.Str()
    steal = fields.Str()
    location = fields.Str()
    disc = fields.Str()