from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.message import Message


class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_message(self, room_id: int, user_id: int, message_text: str) -> Message:
        """Creating a new message in the database"""
        new_message = Message(
            room_id=room_id,
            user_id=user_id,
            message_text=message_text
        )
        self.db.add(new_message)
        await self.db.commit()
        await self.db.refresh(new_message)
        return new_message

    async def get_messages_by_room(self, room_id: int):
        """Receive all messages for the room"""
        result = await self.db.execute(select(Message).filter_by(room_id=room_id))
        return result.scalars().all()
