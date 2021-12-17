import random
import string
import datetime
import jwt
import logging

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.sql.expression import ClauseElement
from fastapi import HTTPException

from app import settings


def number_id_generator(
    session, model, column_name, size=6, chars=string.digits[1:]
):
    random_number = "".join(
        random.SystemRandom().choice(chars) for _ in range(size)
    )
    column = getattr(model, column_name, None)
    number_ex = session.query(model).filter(column == random_number).first()
    if number_ex:
        return number_id_generator(session, model, column_name)
    return random_number


def get_or_create(session, model, schema, data):
    """Get an existing model or create a new one if it does not exist."""
    validation_errors = schema.validate(data)
    if validation_errors:
        raise HTTPException(status_code=422, detail=validation_errors)

    kwargs = {}
    unique_fields = schema.Meta.unique_fields

    instance = None
    if unique_fields is not None and isinstance(unique_fields, (list, tuple)):
        for field in unique_fields:
            field_value = data.get(field)
            if field_value is not None:
                kwargs[field] = field_value

        query = session.query(model)

        # Filter only if kwargs is not empty
        if kwargs:
            query = query.filter_by(**kwargs)
            instance = query.first()

        if instance is not None:
            return False, instance

    params = dict(
        (k, v) for k, v in data.items() if not isinstance(v, ClauseElement)
    )
    instance = schema.load(params)
    instance.save(session)
    return True, instance


def hash_password(password):
    hasher = PasswordHasher()
    hashed_password = hasher.hash(password)
    return hashed_password


def verify_password(password, hash):
    hasher = PasswordHasher()
    try:
        return hasher.verify(hash, password)
    except VerifyMismatchError:
        raise HTTPException(
            status_code=401,
            detail="Please enter the correct username and password",
        )


def generate_access_token(payload):
    now = datetime.datetime.now(datetime.timezone.utc)
    expiration_time = now + datetime.timedelta(hours=12)
    payload["exp"] = expiration_time
    access_token = jwt.encode(
        payload,
        settings.JWT_SECRET,
    )
    return {
        "access_token": access_token,
        "expires_at": str(expiration_time),
        "user_id": payload["user_id"],
        "created_by": "System",
        "updated_by": "System",
    }


def decode_jwt_token(token):
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET)
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Your access token has expired. Please log in again",
        )
    except Exception as exc:
        logging.exception(f"Decode jwt token error: {exc}")
        raise HTTPException(
            status_code=401, detail="Invalid access token. Please log in again"
        )


def format_phone_number(phone_number: str):
    if phone_number.startswith("+"):
        return phone_number
    elif phone_number.startswith("0"):
        phone_number = phone_number[1:]
    return f"+254{phone_number}"
