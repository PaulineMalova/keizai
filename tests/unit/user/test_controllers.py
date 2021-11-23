import json

from uuid import uuid4

from app.user.controllers import UserController


class TestUser:
    @staticmethod
    def test_can_get_multiple_users(session, create_user):
        create_user("+254712345689", "newbe@yahoo.com")
        create_user("+254768901342", "newbie@gmail.com")
        user = json.loads(UserController.fetch_records(session))
        if len(user) != 2:
            raise AssertionError()

    @staticmethod
    def test_can_add_user(session, user):
        result = json.loads(UserController.post_record(session, user))
        if result["user_id"] is None or result.get("password") is not None:
            raise AssertionError()

    @staticmethod
    def test_can_update_user(session, create_user):
        new_user = create_user("+254722345678", "test@yahoo.com")
        updated_user = json.loads(
            UserController.update_record(
                session, {"user_name": "Newbie"}, new_user.user_id
            )
        )
        if updated_user["user_name"] != "Newbie":
            raise AssertionError()

    @staticmethod
    def test_can_get_user(session, create_user):
        new_user = create_user("+254712345679", "new@yahoo.com")
        user = json.loads(
            UserController.fetch_records(session, pk=new_user.user_id)
        )
        if user["user_id"] != str(new_user.user_id):
            raise AssertionError()

    @staticmethod
    def test_can_delete_user(session, create_user):
        new_user = create_user("+254712445689", "newby@yahoo.com")
        deleted_response = json.loads(
            UserController.soft_delete(
                session, pk=new_user.user_id, user_id=str(uuid4())
            )
        )
        if deleted_response["deleted"] is not True:
            raise AssertionError()
