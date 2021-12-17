import functools
import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.user.models import OauthToken
from app.database import create_session
from app.settings import APP_ENVIRONMENT

session: Session = create_session()


def authorize(func):
    @functools.wraps(func)
    async def wrapper(request, *args, **kwargs):
        if APP_ENVIRONMENT.upper() != "DEBUG":
            bearer_token = request.headers.get("authorization")
            if bearer_token is None:
                raise HTTPException(
                    status_code=401, detail="The access token is missing"
                )
            access_token = bearer_token.split(" ")[1]
            user_id = request.headers.get("x-authenticated-userid")
            if user_id is None:
                raise HTTPException(
                    status_code=401,
                    detail="The X-Authenticated-Userid is missing",
                )
            now = str(datetime.datetime.now(datetime.timezone.utc))
            valid_token = (
                session.query(OauthToken)
                .filter(
                    OauthToken.user_id == user_id,
                    OauthToken.access_token == access_token,
                    OauthToken.expires_at > now,
                )
                .first()
            )
            if valid_token is None:
                raise HTTPException(
                    status_code=401,
                    detail="The access token is invalid or expired",
                )

        return await func(request, *args, **kwargs)

    return wrapper
