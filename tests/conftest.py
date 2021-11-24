import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import create_all_tables, drop_all_tables


@pytest.fixture(scope="module")
def session():
    db_url = "postgresql://postgres:password@localhost:5432/keizai_test"
    engine = create_engine(db_url)
    create_all_tables(engine)
    session = sessionmaker(bind=engine)
    yield session()
    drop_all_tables(engine)
