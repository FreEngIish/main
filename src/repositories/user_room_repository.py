from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from db.models.user_room import UserRoom
from exceptions import (
    PermissionDeniedException,
    RoomCreationException,
    RoomGetException,
    RoomNotFoundException,
    RoomUpdateException,
)
from schemas.user_room_schemas import UserRoomCreateSchema, UserRoomUpdateSchema


class UserRoomRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_room(self, room_data: UserRoomCreateSchema, creator_id: int):
        try:
            new_room = UserRoom(
                room_name=room_data.room_name,
                native_language=room_data.native_language,
                language_level=room_data.language_level,
                participant_limit=room_data.participant_limit,
                creator_id=creator_id
            )
            self.db.add(new_room)
            await self.db.commit()
            await self.db.refresh(new_room)
            return new_room
        except IntegrityError:
            await self.db.rollback()
            raise RoomCreationException('Integrity error occurred during room creation.')
        except OperationalError:
            await self.db.rollback()
            raise RoomCreationException('Operational error occurred during room creation.')
        except Exception as e:
             await self.db.rollback()
             raise RoomCreationException(str(e))


    async def get_room_by_id(self, room_id: int):
        try:
            result = await self.db.execute(
                select(UserRoom).where(UserRoom.room_id == room_id).options(joinedload(UserRoom.creator))
            )
            room = result.scalars().first()
            if not room:
                raise RoomNotFoundException
            return room
        except OperationalError:
            raise RoomGetException('Operational error occurred while fetching room')
        except Exception as e:
            raise RoomGetException(str(e))

    async def update_room(self, room_id: int, room_data: UserRoomUpdateSchema, creator_id: int):
        try:
            result = await self.db.execute(select(UserRoom).where(UserRoom.room_id == room_id))
            room = result.scalars().first()

            if not room:
                raise RoomNotFoundException
            if room.creator_id != creator_id:
                raise PermissionDeniedException

            if room_data.room_name:
                room.room_name = room_data.room_name
            if room_data.native_language:
                room.native_language = room_data.native_language
            if room_data.language_level:
                room.language_level = room_data.language_level
            if room_data.participant_limit:
                room.participant_limit = room_data.participant_limit

            await self.db.commit()
            await self.db.refresh(room)
            return room
        except IntegrityError:
            await self.db.rollback()
            raise RoomUpdateException('Integrity error occurred during room update')
        except OperationalError:
            await self.db.rollback()
            raise RoomUpdateException('Operational error occurred during room update')
        except Exception as e:
            await self.db.rollback()
            raise RoomUpdateException(str(e))
