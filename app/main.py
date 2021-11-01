from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import create_session
from app.user import schemas, models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
def main():
    return "Hello World!"


# @app.get("/users/", response_model=List[schemas.UserSchema])
# def show_users(db: Session = create_session()):
#     users = db.query(models.User).all()
#     return users
