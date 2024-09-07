from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from src.db.database import engine, Base, AsyncSessionLocal

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
