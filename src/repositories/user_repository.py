from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db_session = db

    async def add_user_to_db(self, user: User) -> User:
        """Добавляет нового пользователя в базу данных."""
        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)
        return user

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Получает пользователя по его username."""
        query = select(User).where(User.username == username)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Получает пользователя по его email."""
        query = select(User).where(User.email == email)
        result = await self.db_session.execute(query)
        return result.scalars().first()
