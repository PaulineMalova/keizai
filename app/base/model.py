import datetime

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base


class BaseModel:

    __abstract__ = True

    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.datetime.now
    )
    updated_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.datetime.now
    )
    created_by = Column(String, nullable=False)
    updated_by = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


Base = declarative_base(cls=BaseModel)
