import pytest

from uuid import uuid4

from app.user.models import User


@pytest.fixture
def user():
    return {
        "first_name": "Test",
        "last_name": "Test",
        "password": "234561",
        "email_address": "test@gmail.com",
        "phone_number": "+254765754678",
        "user_name": "Test",
        "created_by": str(uuid4()),
        "updated_by": str(uuid4()),
    }


@pytest.fixture
def create_user(session, user):
    session = session

    def _create_user(phone_number, email_address):
        user["phone_number"] = phone_number
        user["email_address"] = email_address
        user["user_number"] = "657893"
        user_instance = User(**user)
        session.add(user_instance)
        session.commit()
        return user_instance

    return _create_user
