from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db.database import get_db
from repositories.auth_repository import AuthRepository
from repositories.user_repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login/google')

def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)

def get_auth_repository() -> AuthRepository:
    return AuthRepository(
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        redirect_uri=settings.google_redirect_uri
    )
