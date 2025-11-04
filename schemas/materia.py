from marshmallow import Schema, fields


class MateriaSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    element = fields.Str(required=True)
    type = fields.Str(required=True)


class GetMateriaSchemaQueries(Schema):
    type = fields.Str(required=False)
    element = fields.Str(required=False)
    sort = fields.Str(required=False)
