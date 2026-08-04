from marshmallow import Schema, fields

class GetUserResponse(Schema):
    user_id = fields.Str(dump_only=True)
    email = fields.Email()
    is_anonymous = fields.Bool()
    last_sign_in_at = fields.DateTime()

class GetUserNotFoundSchema(Schema):
    error = fields.Str(dump_only=True)