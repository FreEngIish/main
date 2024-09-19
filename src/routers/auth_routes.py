from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from schemas.user_schemas import User, Token
from config import settings

router = APIRouter()

oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=settings.google_redirect_uri,
    client_kwargs={'scope': 'openid email profile'}
)

@router.get("/login")
async def login(request: Request):
    redirect_uri = settings.google_redirect_uri
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/oauth/login-success/")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    if not user:
        raise HTTPException(status_code=400, detail="Google authentication failed")
    return User(email=user['email'], name=user['name'])
