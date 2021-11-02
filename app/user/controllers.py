from app.user.models import User
from app.user.schemas import UserSchema
from app.base.controller import BaseController
from app.utils import number_id_generator


class UserController(BaseController):
    model = User
    schema = UserSchema

    @classmethod
    def post_record(cls, session, data, response):
        user_number = data.get("user_number")
        if user_number is None:
            data["user_number"] = number_id_generator(
                session, cls.model, "user_number"
            )
        return super().post_record(session, data, response)
