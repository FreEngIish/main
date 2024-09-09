from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RoomMembersCreateSchema(BaseModel):
    room_id: int

    model_config = ConfigDict(from_attributes=True)  # ORM MODE Pydantic 2.0 версия


class RoomMembersDeleteSchema(BaseModel):
    room_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)  # ORM MODE Pydantic 2.0 версия


class RoomMembersResponseSchema(BaseModel):
    id: int
    room_id: int
    user_id: int
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)  # ORM MODE Pydantic 2.0 версия
