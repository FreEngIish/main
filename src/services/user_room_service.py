from exceptions import (
    PermissionDeniedException,
    RoomCreationException,
    RoomGetException,
    RoomNotFoundException,
    RoomUpdateException,
)
from repositories.user_room_repository import UserRoomRepository
from schemas.user_room_schemas import UserRoomCreateSchema, UserRoomUpdateSchema


class UserRoomService:
    def __init__(self, user_room_repository: UserRoomRepository):
        self.user_room_repository = user_room_repository

    async def create_room(self, room_data: UserRoomCreateSchema, creator_id: int):
        try:
            return await self.user_room_repository.create_room(room_data, creator_id)
        except RoomCreationException:
            raise

    async def get_room(self, room_id: int):
        try:
            return await self.user_room_repository.get_room_by_id(room_id)
        except (RoomNotFoundException, RoomGetException):
            raise

    async def update_room(self, room_id: int, room_data: UserRoomUpdateSchema, creator_id: int):
        try:
            return await self.user_room_repository.update_room(room_id, room_data, creator_id)
        except (RoomNotFoundException, PermissionDeniedException, RoomUpdateException):
            raise
