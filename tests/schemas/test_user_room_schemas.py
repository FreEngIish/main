from datetime import datetime

import pytest
from pydantic import ValidationError

from src.schemas.user_room_schemas import (
    RoomMembersDeleteSchema,
    UserRoomCreateSchema,
    UserRoomResponseSchema,
    UserRoomUpdateSchema,
)


def test_user_room_create_schema_valid():
    data = {
        "room_name": "English Room",
        "native_language": "English",
        "language_level": "Intermediate",
        "participant_limit": 5
    }
    room = UserRoomCreateSchema(**data)
    assert room.room_name == "English Room"
    assert room.native_language == "English"
    assert room.language_level == "Intermediate"
    assert room.participant_limit == 5


def test_user_room_create_schema_default_values():
    data = {
        "room_name": "Spanish Room",
        "native_language": "Spanish"
    }
    room = UserRoomCreateSchema(**data)
    assert room.room_name == "Spanish Room"
    assert room.native_language == "Spanish"
    assert room.language_level == "Beginner"
    assert room.participant_limit == 10


def test_user_room_create_schema_invalid_participant_limit():
    data = {
        "room_name": "French Room",
        "native_language": "French",
        "participant_limit": 12
    }
    with pytest.raises(ValidationError):
        UserRoomCreateSchema(**data)


def test_user_room_update_schema_valid():
    data = {
        "room_name": "Updated Room",
        "language_level": "Advanced",
        "participant_limit": 8,
        "status": "Inactive"
    }
    room = UserRoomUpdateSchema(**data)
    assert room.room_name == "Updated Room"
    assert room.language_level == "Advanced"
    assert room.participant_limit == 8
    assert room.status == "Inactive"


def test_user_room_update_schema_optional():
    data = {}
    room = UserRoomUpdateSchema(**data)
    assert room.room_name is None
    assert room.native_language is None
    assert room.language_level is None
    assert room.participant_limit is None
    assert room.status is None


def test_user_room_update_schema_invalid_participant_limit():
    data = {
        "participant_limit": 15
    }
    with pytest.raises(ValidationError):
        UserRoomUpdateSchema(**data)


def test_user_room_response_schema_valid():
    data = {
        "room_id": 1,
        "room_name": "English Room",
        "creator_id": 1,
        "native_language": "English",
        "language_level": "Intermediate",
        "participant_limit": 10,
        "current_participants": 5,
        "creation_date": datetime.now(),
        "last_updated_date": datetime.now(),
        "status": "Active"
    }
    room = UserRoomResponseSchema(**data)
    assert room.room_id == 1
    assert room.room_name == "English Room"
    assert room.creator_id == 1
    assert room.native_language == "English"
    assert room.language_level == "Intermediate"
    assert room.participant_limit == 10
    assert room.current_participants == 5
    assert room.status == "Active"
    assert isinstance(room.creation_date, datetime)
    assert isinstance(room.last_updated_date, datetime)


def test_user_room_response_schema_missing_last_updated_date():
    data = {
        "room_id": 2,
        "room_name": "French Room",
        "creator_id": 1,
        "native_language": "French",
        "language_level": "Advanced",
        "participant_limit": 7,
        "current_participants": 2,
        "creation_date": datetime.now(),
        "status": "Active"
    }
    room = UserRoomResponseSchema(**data)
    assert room.last_updated_date is None


def test_room_members_delete_schema_valid():
    data = {
        "room_id": 1,
        "user_id": 2
    }
    delete_data = RoomMembersDeleteSchema(**data)
    assert delete_data.room_id == 1
    assert delete_data.user_id == 2


def test_room_members_delete_schema_invalid():
    data = {
        "room_id": "not_a_number",
        "user_id": 2
    }
    with pytest.raises(ValidationError):
        RoomMembersDeleteSchema(**data)
