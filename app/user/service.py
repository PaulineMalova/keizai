import uuid

from fastapi import APIRouter, Request, Response
from sqlalchemy.orm import Session

from app.database import create_session

from app.user.controllers import UserController, AuthController
from app.user.input import PartialUserInput, LoginInput

session: Session = create_session()

router = APIRouter(tags=["users"])


@router.get("/users")
def get_users(request: Request):
    result = UserController.as_view(session, request)
    return result


@router.post("/register")
def create_user(user: PartialUserInput, request: Request, response: Response):
    result = UserController.as_view(
        session, request, item=user, response=response
    )
    return result


@router.get("/users/{user_id}")
def get_user(request: Request, user_id: uuid.UUID, response: Response):
    result = UserController.as_view(
        session, request, pk=user_id, response=response
    )
    return result


@router.put("/users/{user_id}")
def update_user(
    user: PartialUserInput, request: Request, user_id: str, response: Response
):
    result = UserController.as_view(
        session, request, user, pk=user_id, response=response
    )
    return result


@router.delete("/users/{user_id}")
def delete_user(request: Request, user_id: str, response: Response):
    result = UserController.as_view(
        session, request, pk=user_id, response=response
    )
    return result


@router.post("/login")
def login(payload: LoginInput, response: Response):
    result = AuthController.login(session, payload, response)
    return result


# TODO: Exclude password from response
