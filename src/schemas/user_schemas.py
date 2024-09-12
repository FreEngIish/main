import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from validators import validate_password, validate_username


class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=6, max_length=150, description='Username must be between 6 and 150 characters long')  # noqa: E501
    password: str = Field(..., min_length=8, description='Password must be at least 8 characters long')
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50, description='First name must be at most 50 characters long')
    last_name: Optional[str] = Field(None, max_length=50, description='Last name must be at most 50 characters long')

    _validate_password = field_validator('password', mode='before')(validate_password)
    _validate_username = field_validator('username', mode='before')(validate_username)

class UpdateUserRequest(BaseModel):
    username: Optional[str] = Field(None, min_length=6, max_length=150, description='Username must be between 6 and 150 characters long')  # noqa: E501
    password: Optional[str] = Field(None, min_length=8, description='Password must be at least 8 characters long')
    first_name: Optional[str] = Field(None, max_length=50, description='First name must be at most 50 characters long')
    last_name: Optional[str] = Field(None, max_length=50, description='Last name must be at most 50 characters long')

    _validate_password = field_validator('password', mode='before')(validate_password)
    _validate_username = field_validator('username', mode='before')(validate_username)

class ShowUser(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True) # ORM MODE Pydantic2.0 Версія
