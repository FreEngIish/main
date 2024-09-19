from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from config import settings
from repositories.auth_repository import AuthRepository
from schemas.auth_schemas import GoogleLoginResponse
from services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from repositories import auth_repository

router = APIRouter()
auth_repository = AuthRepository(
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
async def auth_google(code: str, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(auth_repository, db)
    try:
        return await auth_service.authenticate_user(code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))