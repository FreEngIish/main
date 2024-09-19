from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models.user import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create_user(self, email: str, name: str):
        new_user = User(email=email, username=name)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
