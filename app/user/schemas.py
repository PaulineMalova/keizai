import uuid

from typing import Optional

from app.base.schema import BaseSchema


class UserSchema(BaseSchema):
    user_id: Optional[uuid.UUID] = uuid.uuid4
    first_name: str
    last_name: str
    user_number: str
    password: str
