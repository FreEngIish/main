from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.database import get_db
from src.schemas.auth_schemas import CreateUserRequest, Token
from src.service.auth_service import AuthService
from src.service.user_service import UserService


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

db_dependency = Annotated[AsyncSession, Depends(get_db)]


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """Dependency for getting the UserService instance."""
    return UserService(db)


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
    auth_service = AuthService()
    token = auth_service.create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
