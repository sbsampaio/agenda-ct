from http import HTTPStatus

from fastapi import FastAPI

from backend.routers import auth, users
from schemas import Message

app = FastAPI(title="Minha API")


app.include_router(auth.router)

app.include_router(users.router)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá Mundo!"}
