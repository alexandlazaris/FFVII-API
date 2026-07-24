from marshmallow import Schema, fields

class SignUpRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class SignUpResponseSchema(Schema):
    email = fields.Email(dumpOnly=True)
    email_verified = fields.Str(dumpOnly=True)

class LoginWithPasswordRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class LoginWithPasswordResponseSchema(Schema):
    access_token = fields.Str(dump_only=True)
    refresh_token = fields.Str(dump_only=True)

class LoginWithPasswordErrorSchema(Schema):
    error = fields.Str(dump_only=True)