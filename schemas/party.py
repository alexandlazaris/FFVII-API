from marshmallow import Schema, fields

from schemas.materia import MateriaSchema

class PartyMemberSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class AssignMateriaSchema(Schema):
    materia_id = fields.List(fields.Str(required=True))

class GetMemberMateriaSchema(Schema):
    member = fields.Nested(PartyMemberSchema)
    materia = fields.Nested(MateriaSchema(many=True))

class GetSingleMemberMateriaSchema(Schema):
    materia = fields.Nested(MateriaSchema(many=True))

class SinglePartyMemberSchema(Schema):
    name = fields.Str(required=True) 