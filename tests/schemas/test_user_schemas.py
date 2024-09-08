import pytest
from pydantic import ValidationError

from src.schemas.user_schemas import CreateUserRequest


def test_valid_user_schema():
    # Тест с валидными данными
    data = {
        "username": "testuser",
        "password": "strongpassword",
        "email": "test@example.com"
    }
    user = CreateUserRequest(**data)
    assert user.username == "testuser"
    assert user.email == "test@example.com"


def test_invalid_email():
    data = {
        "username": "testuser",
        "password": "strongpassword",
        "email": "invalid-email"
    }
    with pytest.raises(ValidationError):
        CreateUserRequest(**data)


def test_missing_field():
    data = {
        "username": "testuser",
        "email": "test@example.com"
    }
    with pytest.raises(ValidationError):
        CreateUserRequest(**data)
