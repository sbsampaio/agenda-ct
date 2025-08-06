from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# from token_settings import TokenSettings

# Usando SQLite temporariamente para evitar problemas de dependências
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
# Para MySQL quando estiver pronto: TokenSettings().DATABASE_URL.replace("mysql+mysqldb", "mysql+aiomysql")

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session
