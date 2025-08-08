from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .base import Base

DATABASE_URL = "sqlite:///./test.db"
# Para MySQL quando estiver pronto: TokenSettings().DATABASE_URL.replace("mysql+mysqldb", "mysql+aiomysql")

engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:  # ← Passe o engine aqui
        yield session