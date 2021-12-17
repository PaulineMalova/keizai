import datetime
import json

from fastapi import HTTPException, status
from sqlalchemy import true

from app.user.models import User, OauthToken
from app.user.schemas import UserSchema, OauthTokenSchema
from app.base.controller import BaseController
from app.utils import (
    number_id_generator,
    hash_password,
    verify_password,
    generate_access_token,
    format_phone_number,
)
from app.account.controllers import AccountController


class UserController(BaseController):
    model = User
    schema = UserSchema
    hide_fields = ["password"]

    @classmethod
    def post_record(cls, session, data, response=None):
        data["user_number"] = number_id_generator(
            session, cls.model, "user_number"
        )
        # Hash password
        password = data.get("password")
        data["password"] = hash_password(password)
        data["phone_number"] = format_phone_number(data["phone_number"])

        schema = cls.schema()
        created, item = cls.perform_post(session, data, schema)
        if created and response is not None:
            response.status_code = status.HTTP_201_CREATED
        if isinstance(cls.hide_fields, list):
            schema = cls.schema(exclude=(field for field in cls.hide_fields))

        # Create user account
        user_id = item.user_id
        AccountController.post_record(
            session,
            {
                "user_id": user_id,
                "created_by": "System",
                "updated_by": "System",
            },
        )

        return schema.dumps(item)

    @classmethod
    def update_record(cls, session, data, pk, response=None):
        if data.get("password") is not None:
            data["password"] = hash_password(data["password"])
        return super().update_record(session, data, pk, response)


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
        phone_number = format_phone_number(data["username"])
        password = str(data["password"])
        user = (
            session.query(User)
            .filter(
                User.phone_number == phone_number,
                User.is_active == true(),
                User.deleted_at.is_(None),
            )
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
            _, item = OauthTokenController.perform_post(
                session, token_data, OauthTokenSchema()
            )
            return OauthTokenSchema(only=["access_token", "user_id"]).dump(
                item
            )

    @classmethod
    def logout(cls, session, user_id, request):
        bearer_token = request.headers["authorization"]
        access_token = bearer_token.split(" ")[1]
        now = str(datetime.datetime.now(datetime.timezone.utc))
        oath_token = (
            session.query(OauthToken)
            .filter(
                OauthToken.user_id == user_id,
                OauthToken.access_token == access_token,
                OauthToken.expires_at > now,
            )
            .first()
        )
        oath_token.delete(synchronize_session_session=False)
        # delete all expired tokens from the db
        cls.delete_expired_access_tokens(session)
        return json.dumps({"success": True})

    @staticmethod
    def delete_expired_access_tokens(session):
        now = str(datetime.datetime.now(datetime.timezone.utc))
        expired_tokens = session.query(OauthToken).filter(
            OauthToken.expires_at <= now
        )
        expired_tokens.delete(synchronize_session=False)
        session.commit()

    @staticmethod
    def reset_password(session, data):
        data = BaseController.get_json_compatible_data(data)
        user = (
            session.query(User)
            .filter(
                User.phone_number == format_phone_number(data["phone_number"]),
                User.email_address == data["email_address"],
            )
            .first()
        )
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if data["new_password"] != data["confirm_password"]:
            raise HTTPException(
                status_code=422,
                detail="New password and confirm password don't match",
            )

        UserController.update_record(
            session,
            {
                "password": data["new_password"],
                "updated_by": str(user.user_id),
            },
            user.user_id,
        )

        return json.dumps({"success": True})
