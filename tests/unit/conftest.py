import pytest

from uuid import uuid4

from app.user.models import User
from app.utils import hash_password


@pytest.fixture(scope="module")
def session_user(session):
    user = User(
        created_by=str(uuid4()),
        updated_by=str(uuid4()),
        first_name="Test",
        last_name="Test",
        password=hash_password("564738"),
        email_address="session.test@gmail.com",
        phone_number="+254768156423",
        user_name="Fixture",
        user_number="567182",
    )
    session.add(user)
    session.commit()
    return user
