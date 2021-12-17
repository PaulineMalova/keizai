import uuid

from fastapi import APIRouter, Request, Response
from sqlalchemy.orm import Session

from app.database import create_session

from app.user.controllers import UserController, AuthController
from app.user.input import PartialUserInput, LoginInput, ResetPasswordInput
from app.auth import authorize

session: Session = create_session()

router = APIRouter(tags=["users"])


@router.get("/users")
@authorize
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
@authorize
def get_user(request: Request, user_id: uuid.UUID, response: Response):
    result = UserController.as_view(
        session, request, pk=user_id, response=response
    )
    return result


@router.put("/users/{user_id}")
def update_user(
    user: PartialUserInput,
    request: Request,
    user_id: uuid.UUID,
    response: Response,
):
    result = UserController.as_view(
        session, request, user, pk=user_id, response=response
    )
    return result


@router.delete("/users/{user_id}")
def delete_user(request: Request, user_id: uuid.UUID, response: Response):
    result = UserController.as_view(
        session, request, pk=user_id, response=response
    )
    return result


@router.post("/login")
def login(payload: LoginInput, response: Response):
    result = AuthController.login(session, payload, response)
    return result


@router.delete("/logout/{user_id}")
@authorize
def logout(request: Request, user_id: uuid.UUID):
    result = AuthController.logout(session, user_id, request)
    return result


@router.post("/reset-password")
def reset_password(payload: ResetPasswordInput):
    result = AuthController.reset_password(session, payload)
    return result
