from datetime import datetime

import pytest
from pydantic import ValidationError

from src.schemas.room_members_schemas import RoomMembersCreateSchema, RoomMembersDeleteSchema, RoomMembersResponseSchema


def test_room_members_create_schema_valid():
    data = {
        "room_id": 1
    }
    schema = RoomMembersCreateSchema(**data)
    assert schema.room_id == 1


def test_room_members_create_schema_invalid():
    data = {
        "room_id": "invalid"
    }
    with pytest.raises(ValidationError):
        RoomMembersCreateSchema(**data)


def test_room_members_delete_schema_valid():
    data = {
        "room_id": 1,
        "user_id": 2
    }
    schema = RoomMembersDeleteSchema(**data)
    assert schema.room_id == 1
    assert schema.user_id == 2


def test_room_members_delete_schema_invalid():
    data = {
        "room_id": 1,
        "user_id": "invalid"
    }
    with pytest.raises(ValidationError):
        RoomMembersDeleteSchema(**data)


def test_room_members_response_schema_valid():
    data = {
        "id": 1,
        "room_id": 2,
        "user_id": 3,
        "joined_at": datetime.now()
    }
    schema = RoomMembersResponseSchema(**data)
    assert schema.id == 1
    assert schema.room_id == 2
    assert schema.user_id == 3
    assert isinstance(schema.joined_at, datetime)


def test_room_members_response_schema_missing_field():
    data = {
        "id": 1,
        "room_id": 2,
        "user_id": 3
    }
    with pytest.raises(ValidationError):
        RoomMembersResponseSchema(**data)
