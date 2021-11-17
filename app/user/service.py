from fastapi import APIRouter, Request, Response
from sqlalchemy.orm import Session

from app.database import create_session

from app.user.schemas import UserSchema, PartialUserSchema, LoginSchema
from app.user.controllers import UserController, AuthController

session: Session = create_session()

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users(request: Request):
    result = UserController.as_view(session, request)
    return result


@router.post("/register")
def create_user(user: UserSchema, request: Request, response: Response):
    result = UserController.as_view(
        session, request, item=user, response=response
    )
    return result


@router.get("/{user_id}")
def get_user(request: Request, user_id: str, response: Response):
    result = UserController.as_view(
        session, request, pk=user_id, response=response
    )
    return result


@router.put("/{user_id}")
def update_user(
    user: PartialUserSchema, request: Request, user_id: str, response: Response
):
    result = UserController.as_view(
        session, request, user, pk=user_id, response=response
    )
    return result


@router.delete("/{user_id}")
def delete_user(request: Request, user_id: str, response: Response):
    result = UserController.as_view(
        session, request, pk=user_id, response=response
    )
    return result


@router.post("/login")
def login(payload: LoginSchema, response: Response):
    result = AuthController.login(session, payload, response)
    return result


# TODO: Exclude password from response
