from typing import Optional

from fastapi import HTTPException
from jose import JWTError, jwt
from starlette import status

from config import settings
from db.models.user import User
from hashing import Hasher
from repositories.user_repository import UserRepository
from schemas.auth_schemas import TokenData


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self.user_repo.get_user_by_username(username=username)
        if not user or not Hasher.verify_password(password, user.hashed_password):
            return None
        return user

    async def get_current_user_from_token(self, token: str) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user.',
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get('sub')
            user_id: int = payload.get('id')
            if username is None or user_id is None:
                raise credentials_exception
            token_data = TokenData(username=username, id=user_id)
        except JWTError:
            raise credentials_exception
        user = await self.user_repo.get_user_by_username(username=token_data.username)
        if user is None:
            raise credentials_exception

        return user
