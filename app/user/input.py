from typing import Optional
from pydantic import BaseModel

from app.base.input import BaseInput


class PartialUserInput(BaseInput):
    first_name: Optional[str]
    last_name: Optional[str]
    user_number: Optional[str]
    password: Optional[str]
    user_name: Optional[str]
    phone_number: Optional[str]
    email_address: Optional[str]


class LoginInput(BaseModel):
    username: str
    password: str


class ResetPasswordInput(BaseModel):
    phone_number: str
    email_address: str
    new_password: str
    confirm_password: str
