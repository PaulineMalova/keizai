import uuid

from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType

from app.base.model import Base


class User(Base):

    __tablename__ = "user"

    user_id = Column(
        UUIDType(binary=False), primary_key=True, default=uuid.uuid4
    )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    user_number = Column(String(6), nullable=False)
    password = Column(String, nullable=False)
