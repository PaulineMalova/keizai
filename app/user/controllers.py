from fastapi import HTTPException

from app.user.models import User, OauthToken
from app.user.schemas import UserSchema, OauthTokenSchema
from app.base.controller import BaseController
from app.utils import (
    number_id_generator,
    hash_password,
    verify_password,
    generate_access_token,
)


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
        # Hash password
        password = data.get("password")
        data["password"] = hash_password(password)

        return super().post_record(session, data, response)


class OauthTokenController(BaseController):
    model = OauthToken
    schema = OauthTokenSchema


class AuthController:
    @classmethod
    def save_access_token(
        session, access_token, user_id, expiration_time, response
    ):
        payload = {
            "user_id": user_id,
            "access_token": access_token,
            "expires_at": expiration_time,
        }
        return OauthTokenController.post_record(session, payload, response)

    @classmethod
    def login(cls, session, data, response):
        data = BaseController.get_json_compatible_data(data)
        phone_number = data["username"]
        password = data["password"]
        user = (
            session.query(User)
            .filter_by(phone_number=phone_number, is_active=True)
            .first()
        )
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User record does not exist. Please register",
            )
        user_id = str(user.user_id)
        if verify_password(password, user.password) is True:
            token_data = generate_access_token({"user_id": user_id})
            result = OauthTokenController.post_record(
                session, token_data, response
            )
            return {"access_token": result.access_token, "user_id": user_id}
