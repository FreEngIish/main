from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.database import get_db
from src.db.models.user import User
from src.schemas.auth_schemas import CreateUserRequest, Token
from src.service.auth_service import authenticate_user, bcrypt_context, create_access_token


router = APIRouter(
    prefix='/auto',
    tags=['auth']
)

db_dependency = Annotated[AsyncSession, Depends(get_db)]

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    create_user_model = User(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        email=create_user_request.email
    )

    db.add(create_user_model)
    await db.commit()
    await db.refresh(create_user_model)
    return create_user_model

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
