from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker, scoped_session

from app import settings
from app.base.model import Base


def db_connect():
    """Create db engine."""
    return create_engine(URL(**settings.DATABASE), poolclass=NullPool)


def create_all_tables(engine):
    """Manually create all db tables."""
    Base.metadata.create_all(engine)


def create_session():
    """Create a sharable db session."""
    engine = db_connect()
    create_all_tables(engine)
    return scoped_session(
        sessionmaker(autocommit=True, autoflush=True, bind=engine)
    )
