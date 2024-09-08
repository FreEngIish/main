from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.service.auth_service import AuthService
from src.service.user_service import UserService


# Dependency for getting the UserService instance
async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)

# General database dependency
db_dependency = Annotated[AsyncSession, Depends(get_db)]

user_dependency = Annotated[dict, Depends(AuthService.get_current_user)]
