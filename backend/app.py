from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.routers import agenda, auth, users
from fast_zero.schemas import Message

app = FastAPI(title="Minha API")


app.include_router(auth.router)

app.include_router(users.router)
app.include_router(agenda.router)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá Mundo!"}
