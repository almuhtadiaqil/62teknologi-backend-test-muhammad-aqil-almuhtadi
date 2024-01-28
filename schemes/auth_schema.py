from marshmallow import Schema, fields, validate, validates


class LoginSchema(Schema):
    email = fields.String(required=True, validate=[validate.Email()])
    password = fields.String(
        required=True, validate=[validate.Length(min=8)], load_only=True
    )

    class Meta:
        strict = True


class RegisterSchema(Schema):
    full_name = fields.String(required=True)
    email = fields.String(required=True, validate=[validate.Email()])
    password = fields.String(
        required=True, validate=[validate.Length(min=8)], load_only=True
    )


class LoginResponseSchema(Schema):
    access_token = fields.String()
    expiration_time = fields.DateTime()
