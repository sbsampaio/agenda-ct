
import os
from contextlib import contextmanager
from datetime import datetime

from fastapi.concurrency import asynccontextmanager
# sqlite para testes
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

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

    from fastapi import FastAPI
    from backend.routers.auth import router as auth_router
    from backend.routers.users import router as users_router
    from backend.routers.appointment import router as appointments_router
    from backend.routers.room import router as room_router
    from backend.db_utils import ensure_default_roles
    from backend.schemas import Message
    from http import HTTPStatus

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        session = next(get_session())
        try:
            ensure_default_roles(session)
            print("✅ Inicialização das roles padrão concluída!")
        finally:
            session.close()
        
        yield
    
    test_app = FastAPI(title="Minha API - Teste")
    test_app.include_router(auth_router)
    test_app.include_router(users_router)
    test_app.include_router(appointments_router)
    test_app.include_router(room_router)

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
        # força o PRAGMA para sqlite
        conn.execute(text("PRAGMA foreign_keys=ON"))
        Base.metadata.create_all(conn)
        
        # depois tenho q ver melhor sobre isso aqui, mas basicamente
        # corrige todas as tabelas com bigint para INTEGER PRIMARY KEY AUTOINCREMENT
        tables_to_fix = ['user', 'role', 'user_role', 'room', 'appointment']
        
        for table_name in tables_to_fix:
            try:
                result = conn.execute(text(f"PRAGMA table_info({table_name})"))
                columns = list(result)
                
                # verifica se tem coluna id com bigint
                id_column = next((col for col in columns if col[1] == 'id'), None)
                if id_column and 'BIGINT' in id_column[2]:
                    # drop e recria a tabela específica
                    if table_name == 'user':
                        conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
                        conn.execute(text("""
                            CREATE TABLE user (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                email VARCHAR(150) NOT NULL UNIQUE,
                                password VARCHAR(255) NOT NULL,
                                first_name VARCHAR(50) NOT NULL,
                                last_name VARCHAR(50) NOT NULL
                            )
                        """))
                    elif table_name == 'role':
                        conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
                        conn.execute(text("""
                            CREATE TABLE role (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name VARCHAR(50) NOT NULL
                            )
                        """))
                    elif table_name == 'user_role':
                        conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
                        conn.execute(text("""
                            CREATE TABLE user_role (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER NOT NULL,
                                role_id INTEGER NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES user(id),
                                FOREIGN KEY (role_id) REFERENCES role(id)
                            )
                        """))
            except Exception as e:
                print(f"Aviso: Erro ao corrigir tabela {table_name}: {e}")
                continue

    with Session(engine, expire_on_commit=False) as session:
        # cria as roles padrao para os testes
        from backend.db_utils import ensure_default_roles
        ensure_default_roles(session)
        
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
    return response.json()["access_token"]


class UserFactory(factory.Factory):
    class Meta:
        model = User

    first_name = factory.Sequence(lambda n: f"teste{n}")
    last_name = factory.Sequence(lambda n: f"lastname{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.first_name}@teste.com")
    password = factory.LazyAttribute(lambda obj: f"{obj.first_name}@example.com")
