from marshmallow import Schema, fields

# --------------- Characters
class CharactersSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)
    weapon = fields.Str(dump_only=True)

# --------------- Party

class PartyMemberSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class AssignMateriaSchema(Schema):
    materia_id = fields.List(fields.Str(required=True))
    member_id = fields.Str()

# --------------- Generic

class DeleteSchema(Schema):
    message = fields.Str(dump_only=True)

# --------------- Enemies

class EnemySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    hp = fields.Int()
    description = fields.Str()
    steal = fields.Str()
    location = fields.Str()
    disc = fields.Str()

# --------------- Materia

class MateriaSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    element = fields.Str(required=True)
    level = fields.Int(required=True)
