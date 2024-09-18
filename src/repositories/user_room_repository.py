from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.user_room import UserRoom


class UserRoomRepository:
    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def add_room(self, room: UserRoom) -> UserRoom:
        self.db_session.add(room)
        await self.db_session.commit()
        await self.db_session.refresh(room)
        return room

    async def get_room_by_id(self, room_id: int) -> Optional[UserRoom]:
        query = select(UserRoom).where(UserRoom.id == room_id)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_rooms_by_user_id(self, user_id: int) -> List[UserRoom]:
        query = select(UserRoom).where(UserRoom.user_id == user_id)
        result = await self.db_session.execute(query)
        return result.scalars().all()
