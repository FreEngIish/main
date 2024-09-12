import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from config import LETTER_MATCH_PATTERN


class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=6, max_length=150, description='Username must be between 6 and 150 characters long')  # noqa: E501
    password: str = Field(..., min_length=8, description='Password must be at least 8 characters long')
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50, description='First name must be at most 50 characters long')
    last_name: Optional[str] = Field(None, max_length=50, description='Last name must be at most 50 characters long')

    @field_validator('password', mode='before')
    def validate_password(cls, value: str) -> str:
        if not re.search(r'[A-Z]', value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', value):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', value):
            raise ValueError('Password must contain at least one digit')
        return value

    @field_validator('username', mode='before')
    def validate_username(cls, value: str) -> str:
        if not LETTER_MATCH_PATTERN.match(value):
            raise ValueError('Username can only contain letters and numbers')
        return value

class UpdateUserRequest(BaseModel):
    username: Optional[str] = Field(None, min_length=6, max_length=150, description='Username must be between 6 and 150 characters long')  # noqa: E501
    password: Optional[str] = Field(None, min_length=8, description='Password must be at least 8 characters long')
    first_name: Optional[str] = Field(None, max_length=50, description='First name must be at most 50 characters long')
    last_name: Optional[str] = Field(None, max_length=50, description='Last name must be at most 50 characters long')

    @field_validator('password', mode='before')
    def validate_password(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            if not re.search(r'[A-Z]', value):
                raise ValueError('Password must contain at least one uppercase letter')
            if not re.search(r'[a-z]', value):
                raise ValueError('Password must contain at least one lowercase letter')
            if not re.search(r'\d', value):
                raise ValueError('Password must contain at least one digit')
        return value

    @field_validator('username', mode='before')
    def validate_username(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            if not LETTER_MATCH_PATTERN.match(value):
                raise ValueError('Username can only contain letters and numbers')
        return value


class ShowUser(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True) # ORM MODE Pydantic2.0 Версія
