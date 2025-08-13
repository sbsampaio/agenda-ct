from contextlib import asynccontextmanager
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models import User, Role, UserRole, Room, Appointment

from backend.routers.auth import router as auth_router
from backend.routers.users import router as users_router
from backend.routers.appointment import router as appointments_router
from backend.routers.room import router as room_router
from backend.schemas import Message
from backend.database import get_session
from backend.db_utils import ensure_default_roles


@asynccontextmanager
async def lifespan(app: FastAPI):
    session = next(get_session())
    try:
        ensure_default_roles(session)
        print("✅ Inicialização das roles padrão concluída!")
    finally:
        session.close()
    
    yield


app = FastAPI(title="Minha API", lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)

app.include_router(users_router)

app.include_router(appointments_router)

app.include_router(room_router)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá Mundo!"}
