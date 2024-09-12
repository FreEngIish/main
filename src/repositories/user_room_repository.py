from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user_room import UserRoom


class UserRoomRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_room(self, room_name: str, creator_id: int, native_language: str, language_level: str = 'Beginner', participant_limit: int = 10):
        """Asynchronous creation of a new room in the database"""
        new_room = UserRoom(
            room_name=room_name,
            creator_id=creator_id,
            native_language=native_language,
            language_level=language_level,
            participant_limit=participant_limit
        )
        self.db.add(new_room)
        await self.db.commit()
        await self.db.refresh(new_room)
        return new_room

    async def get_room(self, room_id: int):
        """Asynchronous room retrieval by ID"""
        return await self.db.get(UserRoom, room_id)

    async def update_participants_count(self, room_id: int, new_count: int):
        """Asynchronous update of the number of participants in the room"""
        room = await self.get_room(room_id)
        if room:
            room.current_participants = new_count
            await self.db.commit()
            await self.db.refresh(room)
            return room
        return None

    async def get_all_rooms(self):
        """Получение всех комнат через ORM"""
        result = await self.db.execute(text("SELECT * FROM user_rooms"))
        rooms = result.fetchall()
        return rooms
