
import os
from contextlib import contextmanager
from datetime import datetime

# Configura SQLite para testes antes de qualquer importação do backend
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

# Adiciona o diretório raiz do projeto ao sys.path
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event, create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from backend.app import app
from backend.database import get_session
from backend.models import User
from backend.base import Base
from backend.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    # Cria uma versão do app sem lifespan para testes
    from fastapi import FastAPI
    from backend.routers.auth import router as auth_router
    from backend.routers.users import router as users_router
    from backend.routers.appointment import router as appointments_router
    from backend.routers.room import router as room_router
    from backend.schemas import Message
    from http import HTTPStatus
    
    test_app = FastAPI(title="Minha API - Teste")
    test_app.include_router(auth_router)
    test_app.include_router(users_router)
    test_app.include_router(appointments_router)
    test_app.include_router(room_router)
    
    @test_app.get("/", status_code=HTTPStatus.OK, response_model=Message)
    def read_root():
        return {"message": "Olá Mundo!"}

    with TestClient(test_app) as client:
        test_app.dependency_overrides[get_session] = get_session_override
        yield client

    test_app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    with engine.begin() as conn:
        # Força o PRAGMA para SQLite
        conn.execute(text("PRAGMA foreign_keys=ON"))
        Base.metadata.create_all(conn)

    with Session(engine, expire_on_commit=False) as session:
        yield session

    with engine.begin() as conn:
        Base.metadata.drop_all(conn)


@pytest.fixture
def user(session):
    password = "testtest"
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def other_user(session):
    password = "testtest"
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, "created_at"):
            target.created_at = time

    event.listen(model, "before_insert", fake_time_hook)

    yield time

    event.remove(model, "before_insert", fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def token(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": user.clean_password},
    )
    # print("Response status code:", response.status_code)
    # print("Response JSON:", response.json())
    return response.json()["access_token"]


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n + 1)
    first_name = factory.Sequence(lambda n: f"test{n}")
    last_name = factory.Sequence(lambda n: f"lastname{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.first_name}@test.com")
    password = factory.LazyAttribute(lambda obj: f"{obj.first_name}@example.com")
