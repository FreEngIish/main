import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db.database import get_db
from repositories.auth_repository import AuthRepository
from repositories.user_repository import UserRepository
from schemas.auth_schemas import GoogleLoginResponse
from services.auth_service import AuthService


# Define a function to provide UserRepository as a dependency
def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Define a function to provide AuthRepository as a dependency
def get_auth_repository() -> AuthRepository:
    return AuthRepository(
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        redirect_uri=settings.google_redirect_uri
    )

@router.get('/auth/login/google')
async def google_login():
    google_auth_url = (
        f'https://accounts.google.com/o/oauth2/auth?client_id={settings.google_client_id}'
        f'&redirect_uri={settings.google_redirect_uri}&response_type=code'
        f'&scope=openid email profile&access_type=offline&approval_prompt=force'
    )
    return RedirectResponse(url=google_auth_url)

@router.get('/auth/oauth/login-success', response_model=GoogleLoginResponse)
async def auth_google(
    code: str,
    auth_repository: AuthRepository = Depends(get_auth_repository),
    user_repository: UserRepository = Depends(get_user_repository)
):
    auth_service = AuthService(auth_repository, user_repository)
    try:
        response = await auth_service.authenticate_user(code)
        return response
    except Exception as e:
        logger.error(f'Failed to authenticate user: {e}')
        raise HTTPException(status_code=400, detail='Authentication failed. Please try again.')
