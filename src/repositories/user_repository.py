from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create_user(self, email: str, first_name: str, last_name: str, google_sub: str, picture: str, locale: str):  # noqa: E501
        new_user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            google_sub=google_sub,
            picture=picture,
            locale=locale
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
