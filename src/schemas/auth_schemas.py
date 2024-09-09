from typing import Optional

from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class ShowUser(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        orm_mode = True

class RefreshTokenRequest(BaseModel):
    refresh_token: str
