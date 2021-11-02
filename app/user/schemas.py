from typing import Optional

from app.base.schema import BaseSchema
from app.user.models import User


class UserSchema(BaseSchema):
    first_name: str
    last_name: str
    user_number: Optional[str]
    password: str
    user_name: str
    phone_number: str
    email_address: str

    class Meta:
        model = User
        unique_fields = ["phone_number", "email_address"]


class PartialUserSchema(UserSchema):
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    user_name: Optional[str]
    phone_number: Optional[str]
    email_address: Optional[str]
