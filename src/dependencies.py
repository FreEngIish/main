from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db.database import get_db
from repositories.auth_repository import AuthRepository
from repositories.user_repository import UserRepository
from validators import validate_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login/google')

def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)

def get_auth_repository() -> AuthRepository:
    return AuthRepository(
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        redirect_uri=settings.google_redirect_uri
    )

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository)
):
    token_data = await validate_access_token(token)

    # We assume that the email is in token_data
    user = await user_repository.get_user_by_email(token_data['email'])

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')

    return user.id
