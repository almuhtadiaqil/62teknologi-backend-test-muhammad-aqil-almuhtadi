from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    full_name = fields.String(required=True)
    email = fields.String(required=True, validate=[validate.Email])
    password = (
        fields.String(
            required=True,
            validate=[validate.Length(min=8)],
            load_only=True,
        ),
    )
    created_at = fields.String()
    updated_at = fields.String()

    class Meta:
        strict = True
