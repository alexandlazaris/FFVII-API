from typing import Optional
from pydantic import BaseModel
from marshmallow import Schema, fields
from uuid import UUID


class SaveRequestSchema(Schema):
    location = fields.Str(required=True)


class SaveResponseSchema(Schema):
    id = fields.Str(dump_only=True)
    location = fields.Str(required=True)
    party = fields.List(fields.Str(dump_only=True))
    party_lead = fields.Dict(dump_only=True)


class SaveItemCreateRequest(BaseModel):
    location: str
    disc: int = 1


class SaveItemCreateResponse(BaseModel):
    location: str
    id: UUID
    disc: int
    user_id: UUID


class PartyLead(BaseModel):
    name: str | None = None
    level: int | None = None


class PartyResult(BaseModel):
    id: UUID | None = None
    lead: PartyLead | None = None
    members: list[str] | None = None


class GetSaveItemResponse(BaseModel):
    location: str
    id: UUID
    disc: int
    user_id: UUID
    party: Optional[PartyResult] = None


class DeleteSaveResponse(BaseModel):
    message: str


class GetAllSaves(BaseModel):
    saves: list[GetSaveItemResponse]
