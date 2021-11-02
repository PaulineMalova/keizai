import uuid

from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType

from app.base.model import Base


class User(Base):

    __tablename__ = "user"

    user_id = Column(
        UUIDType(binary=False),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    user_number = Column(String(6), nullable=False)
    password = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    email_address = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return str(self.user_id)
