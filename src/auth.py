from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt

from config import settings


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    data = {
        'sub': username,
        'id': user_id
    }
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    data.update({'exp': expire})
    encoded_jwt = jwt.encode(
        data, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
