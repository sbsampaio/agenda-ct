from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .base import Base
from .token_settings import TokenSettings

# DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = DATABASE_URL(self)
# Para MySQL quando estiver pronto: TokenSettings().DATABASE_URL.replace("mysql+mysqldb", "mysql+aiomysql")

engine = create_engine(TokenSettings().DATABASE_URL)

print(f"URL de conexão usada: {engine.url}")


def get_session():
    with Session(engine) as session:  # ← Passe o engine aqui
        yield session