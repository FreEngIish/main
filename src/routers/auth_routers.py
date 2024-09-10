from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from security import create_access_token
from config import settings
from dependencies import get_auth_service
from schemas.auth_schemas import Token
from services.auth_services import AuthService


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/token', response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
) -> Token:
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={'sub': user.username, 'id': user.id},
        expires_delta=access_token_expires
    )

    return {'access_token': token, 'token_type': 'bearer'}
