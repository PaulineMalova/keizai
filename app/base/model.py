import datetime
import logging

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

from app.exceptions import DatabaseError


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
    deleted_by = Column(String, nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def save(self, session):
        try:
            session.add(self)
            session.commit()
        except Exception as exc:
            session.rollback()
            logging.exception(exc)
            raise DatabaseError(
                f"Problem saving {self.__class__.__name__} record in database"
            )

    def get(self, session, pk):
        """
        Get a single record given a pk
        """
        return session.query(self).get(pk)

    def delete(self, session, updated_by):
        """Delete a record from the database."""
        self.deleted_at = datetime.datetime.now()
        self.active = False
        self.deleted_by = updated_by
        self.save(session)

    def set_model_dict(self, model_dict):
        """Set Model Attributes from dict."""
        for k, v in model_dict.items():
            getattr(self, k, setattr(self, k, v))


Base = declarative_base(cls=BaseModel)
