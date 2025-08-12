from contextlib import asynccontextmanager
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


from http import HTTPStatus

from fastapi import FastAPI

from backend.models import User, Role, UserRole, Room, Appointments

from backend.routers.auth import router as auth_router
from backend.routers.users import router as users_router
from backend.routers.appointments import router as appointments_router
from backend.routers.room import router as room_router
from backend.schemas import Message
from backend.database import get_session
from backend.db_utils import ensure_default_roles

app = FastAPI(title="Minha API")


# corrigit o deprecated
@asynccontextmanager("startup")
async def startup_event():
    session = next(get_session())
    try:
        ensure_default_roles(session)
        print("✅ Inicialização das roles padrão concluída!")
    finally:
        session.close()


app.include_router(auth_router)

app.include_router(users_router)

app.include_router(appointments_router)

app.include_router(room_router)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá Mundo!"}
