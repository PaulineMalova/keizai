from typing import Optional

from app.base.input import BaseInput


class PartialUserInput(BaseInput):
    first_name: Optional[str]
    last_name: Optional[str]
    user_number: Optional[str]
    password: Optional[str]
    user_name: Optional[str]
    phone_number: Optional[str]
    email_address: Optional[str]


class LoginInput(BaseInput):
    username: str
    password: str
