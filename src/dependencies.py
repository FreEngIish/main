from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from db.models.user import User
from repositories.user_repository import UserRepository
from services.auth_services import AuthService
from services.user_services import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(session=session)

async def get_user_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repo=user_repo)

async def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repo=user_repo)

async def get_current_user(
    auth_service: AuthService = Depends(get_auth_service), token: str = Depends(oauth2_scheme)
) -> User:
    return await auth_service.get_current_user_from_token(token=token)

