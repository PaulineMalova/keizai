from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.user import service as user_service


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(user_service.router)


@app.get("/")
def main():
    return "Hello World!"
