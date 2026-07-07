from marshmallow import Schema, fields

class SignUpRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class SignUpResponseSchema(Schema):
    email = fields.Email(dumpOnly=True)
