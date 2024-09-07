from databases import Database
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite+aiosqlite:///./test.db'

# Асинхронная база данных
database = Database(DATABASE_URL)
metadata = MetaData()

# Асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Используем асинхронный sessionmaker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

Base = declarative_base()

# Пример использования
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
        
async def init_db():
    async with engine.begin() as conn:
        # Создаем все таблицы в базе данных
        await conn.run_sync(Base.metadata.create_all)