from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.dependencies import db_dependency, get_user_service
from src.schemas.auth_schemas import CreateUserRequest, RefreshTokenRequest, Token
from src.service.auth_service import AuthService
from src.service.user_service import UserService
from src.settings import Settings


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest,
                      user_service: UserService = Depends(get_user_service)):
    """Creates a new user using the service layer."""
    return await user_service.create_user(create_user_request)


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    auth_service = AuthService()
    user = await auth_service.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')
    access_token = auth_service.create_access_token(
        user.username, user.id, timedelta(minutes=Settings.TIME_TO_RENEW_ACCESS)
        )
    refresh_token = auth_service.create_refresh_token(
        user.username, user.id, timedelta(days=Settings.TIME_TO_RENEW_REFRESH)
        )
    return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer'
            }


@router.post('/refresh', response_model=Token)
async def refresh_access_token(request: RefreshTokenRequest, db: db_dependency):  # noqa: ARG001
    auth_service = AuthService()
    user_data = auth_service.verify_refresh_token(request.refresh_token)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid refresh token')
    access_token = auth_service.create_access_token(
        user_data['username'], user_data['id'], timedelta(minutes=Settings.TIME_TO_RENEW_ACCESS)
        )
    refresh_token = auth_service.create_refresh_token(
        user_data['username'], user_data['id'], timedelta(days=Settings.TIME_TO_RENEW_REFRESH)
        )
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
            }
