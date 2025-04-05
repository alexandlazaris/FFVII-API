from marshmallow import Schema, fields

from schemas.characters import *
from schemas.materia import *
from schemas.enemy import *
from schemas.party import *

# --------------- Generic

class DeleteSchema(Schema):
    message = fields.Str(dump_only=True)

