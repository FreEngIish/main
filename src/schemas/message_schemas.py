from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MessageCreateSchema(BaseModel):
    room_id: int
    message_text: str

    model_config = ConfigDict(from_attributes=True) # ORM MODE Pydantic2.0 Версія


class MessageUpdateSchema(BaseModel):
    message_text: Optional[str] = None

    model_config = ConfigDict(from_attributes=True) # ORM MODE Pydantic2.0 Версія


class MessageResponseSchema(BaseModel):
    message_id: int
    room_id: int
    user_id: int
    message_text: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True) # ORM MODE Pydantic2.0 Версія
