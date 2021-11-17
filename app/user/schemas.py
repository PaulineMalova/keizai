from marshmallow import fields

from app.base.schema import BaseSchema
from app.user.models import User, OauthToken


class UserSchema(BaseSchema):
    user_id = fields.UUID(dump_only=True)
    first_name = fields.Str(
        required=True, error_messages={"required": "First name is required"}
    )
    last_name = fields.Str(
        required=True, error_messages={"required": "Last name is required"}
    )
    user_number = fields.Str(
        required=True, error_messages={"required": "User number is required"}
    )
    password = fields.Str(
        required=True, error_messages={"required": "Password is required"}
    )
    user_name = fields.Str(
        required=True, error_messages={"required": "User name is required"}
    )
    phone_number = fields.Str(
        required=True, error_messages={"required": "Phone number is required"}
    )
    email_address = fields.Str(
        required=True, error_messages={"required": "Email address is required"}
    )

    class Meta(BaseSchema.Meta):
        model = User
        unique_fields = ["phone_number", "email_address"]


class OauthTokenSchema(BaseSchema):
    oauth_token_id = fields.UUID(dump_only=True)
    user_id = fields.UUID(required=True)
    access_token = fields.Str(required=True)
    expires_at = fields.DateTime(required=True)

    class Meta(BaseSchema.Meta):
        model = OauthToken
