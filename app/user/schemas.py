# TODO: Use Marshmallow in place of pydantic

import uuid

from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.base.schema import BaseSchema
from app.user.models import User, OauthToken


class UserSchema(BaseSchema):
    first_name: str
    last_name: str
    user_number: Optional[str]
    password: str
    user_name: str
    phone_number: str
    email_address: str

    class Meta(BaseSchema.Meta):
        model = User
        unique_fields = ["phone_number", "email_address"]


class PartialUserSchema(UserSchema):
    first_name: Optional[str]
    last_name: Optional[str]
    user_name: Optional[str]
    phone_number: Optional[str]
    email_address: Optional[str]


class OauthTokenSchema(BaseSchema):
    user_id: uuid.UUID
    access_token: str
    expires_at: datetime

    class Meta(BaseSchema.Meta):
        model = OauthToken


class LoginSchema(BaseModel):
    username: str
    password: str
