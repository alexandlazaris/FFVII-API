from marshmallow import Schema, fields
from pydantic import BaseModel, Field
from typing import Optional

# smorest compatible schema
class EnemySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    hp = fields.Int()
    description = fields.Str()
    steal = fields.Str()
    location = fields.Str()
    disc = fields.Str()


# could be removed, not the most useful
class EnemyDeleted(Schema):
    message = fields.Str()

class EnemyBase(BaseModel):
    """Base schema with common fields for enemy creation/updates"""
    name: str = Field(..., min_length=1, max_length=30)
    hp: int = Field(..., gt=0)
    description: Optional[str] = None
    steal: Optional[str] = None
    location: str = Field(..., min_length=1)
    disc: str = Field(..., min_length=1)

# pydantic model used to transform incoming json
class EnemyCreate(EnemyBase):
    """Schema for creating a new enemy"""
    pass

# pydantic model used to transform incoming json
class EnemyUpdate(BaseModel):
    """Schema for updating an enemy (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=30)
    hp: Optional[int] = Field(None, gt=0)
    description: Optional[str] = None
    steal: Optional[str] = None
    location: Optional[str] = Field(None, min_length=1)
    disc: Optional[str] = Field(None, min_length=1)