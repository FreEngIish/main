from datetime import datetime, timedelta
from typing import Annotated, Dict, Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from db.models.user import User
from config import settings


class AuthService:
    def __init__(self):
        self.bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    async def get_current_user(token: Annotated[
        str, Depends(OAuth2PasswordBearer(tokenUrl='auth/token'))
        ]
        ) -> Dict[str, Optional[str]]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get('sub')
            user_id: int = payload.get('id')
            if username is None or user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='Could not validate user.')
            return {'username': username, 'id': user_id}
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')

    async def authenticate_user(self, username: str, password: str, db: AsyncSession) -> Optional[User]:
        stmt = select(User).filter(User.username == username)
        result = await db.execute(stmt)
        user = result.scalars().first()
        if not user or not self.bcrypt_context.verify(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, username: str, user_id: int, expires_delta: timedelta) -> str:
        encode = {'sub': username, 'id': user_id}
        expires = datetime.utcnow() + expires_delta
        encode.update({'exp': expires})
        return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

auth_service = AuthService()
