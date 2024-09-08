from datetime import datetime

import pytest
from pydantic import ValidationError

from src.schemas.message_schemas import MessageCreateSchema, MessageResponseSchema, MessageUpdateSchema


def test_message_create_schema_valid():
    data = {
        "room_id": 1,
        "message_text": "Hello, this is a test message."
    }
    message = MessageCreateSchema(**data)
    assert message.room_id == 1
    assert message.message_text == "Hello, this is a test message."


def test_message_create_schema_invalid():
    data = {
        "message_text": "Hello, this is a test message."
    }
    with pytest.raises(ValidationError):
        MessageCreateSchema(**data)


def test_message_update_schema_valid():
    data = {
        "message_text": "Updated message text."
    }
    message = MessageUpdateSchema(**data)
    assert message.message_text == "Updated message text."


def test_message_update_schema_optional():
    data = {}
    message = MessageUpdateSchema(**data)
    assert message.message_text is None


def test_message_response_schema_valid():
    data = {
        "message_id": 1,
        "room_id": 1,
        "user_id": 1,
        "message_text": "Response message text",
        "timestamp": datetime.now()
    }
    message = MessageResponseSchema(**data)
    assert message.message_id == 1
    assert message.room_id == 1
    assert message.user_id == 1
    assert message.message_text == "Response message text"
    assert isinstance(message.timestamp, datetime)
