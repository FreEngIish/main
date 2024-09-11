from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def add_user_to_db(self, user: User) -> User:
        """Adds a new user to the database."""
        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user from the database by their ID.
        """
        query = select(User).where(User.id == user_id)
        result = await self.db_session.execute(query)
        user = result.scalars().first()
        return user

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieves a user by their username."""
        query = select(User).where(User.username == username)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieves a user by their email."""
        query = select(User).where(User.email == email)
        result = await self.db_session.execute(query)
        return result.scalars().first()
    
    async def update_user(self, user: User) -> User:
        """Updates an existing user in the database."""
        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)
        return user

    async def delete_user(self, user: User) -> None:
        """Deletes a user from the database."""
        await self.db_session.delete(user)
        await self.db_session.commit()