from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, conint


class LanguageLevel(str, Enum):
    beginner = 'Beginner'
    intermediate = 'Intermediate'
    advanced = 'Advanced'
    proficient = 'Proficient'


class UserRoomCreateSchema(BaseModel):
    room_name: str
    native_language: str
    language_level: Optional[LanguageLevel] = LanguageLevel.beginner
    participant_limit: Optional[conint(ge=2, le=10)] = 10 # type: ignore

    model_config = ConfigDict(from_attributes=True) # ORM MODE Pydantic2.0 Версія


class UserRoomUpdateSchema(BaseModel):
    room_name: Optional[str] = None
    native_language: Optional[str] = None
    language_level: Optional[LanguageLevel] = None
    participant_limit: Optional[conint(ge=2, le=10)] = None # type: ignore
    status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True) # ORM MODE Pydantic2.0 Версія


class UserRoomResponseSchema(BaseModel):
    room_id: int
    room_name: str
    creator_id: int
    native_language: str
    language_level: LanguageLevel
    participant_limit: int
    current_participants: int
    creation_date: datetime
    last_updated_date: Optional[datetime] = None
    status: str

    model_config = ConfigDict(from_attributes=True) # ORM MODE Pydantic2.0 Версія


class RoomMembersDeleteSchema(BaseModel):
    room_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True) # ORM MODE Pydantic2.0 Версія
