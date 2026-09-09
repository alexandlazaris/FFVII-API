from marshmallow import Schema, fields
from schemas.materia import MateriaSchema
from pydantic import BaseModel
from uuid import UUID

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

class PartyMemberRequestSchema(Schema):
    name = fields.Str(required=True)

class PartyMemberResponseSchema(Schema):
    name = fields.Str()
    level = fields.Str()

class PartyRequest(BaseModel):
    name: str

class PartyMemberObj(BaseModel):
    name: str
    level: int

class PartyMemberList(BaseModel):
    name: str
    level: int

CreatePartyRequest = list[PartyRequest]

class PartyResponse(BaseModel):
    party: list[PartyMemberObj]
    id: UUID