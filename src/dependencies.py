from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from repositories.user_repository import UserRepository
from service.auth_service import AuthService
from service.user_service import UserService


def get_user_repository(session: AsyncSession = Depends(get_db)):
    return UserRepository(session=session)


# Dependency for getting the UserService instance
async def get_user_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repo=user_repo)


# General database dependency
db_dependency = Annotated[AsyncSession, Depends(get_db)]

user_dependency = Annotated[dict, Depends(AuthService.get_current_user)]
