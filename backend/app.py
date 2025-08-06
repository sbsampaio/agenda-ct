import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


from http import HTTPStatus

from fastapi import FastAPI

from backend.routers.auth import router as auth_router
from backend.routers.users import router as users_router
from backend.schemas import Message

app = FastAPI(title="Minha API")


app.include_router(auth_router)

app.include_router(users_router)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá Mundo!"}
