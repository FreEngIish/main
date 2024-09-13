import logging

from db import User
from repositories.user_room_repository import UserRoomRepository
from schemas.user_room_schemas import UserRoomCreateSchema, UserRoomResponseSchema
from services.socket_service import ConnectionManager


logger = logging.getLogger(__name__)


class RoomManagerService:
    def __init__(self, room_repo: UserRoomRepository, socket_service: ConnectionManager):
        self.room_repo = room_repo
        self.socket_service = socket_service

    async def get_all_rooms(self):
        """Fetch all rooms."""
        try:
            rooms = await self.room_repo.get_all_rooms()
            return [UserRoomResponseSchema.from_orm(room) for room in rooms]
        except Exception as e:
            logger.error(f'Error fetching rooms: {e}')
            raise

    async def create_room(self, room_request: UserRoomCreateSchema, creator: User):
        """Create a new room and notify all clients."""
        try:
            new_room = await self.room_repo.create_room(
                room_name=room_request.room_name, creator_id=creator.id, native_language=room_request.native_language
            )
            await self.notify_all_clients_about_rooms()
            return new_room
        except Exception as e:
            logger.error(f'Error creating room: {e}')
            raise

    async def notify_all_clients_about_rooms(self):
        """Notify all connected users about room updates"""
        try:
            rooms_data = await self.get_all_rooms()
            message = [room.json() for room in rooms_data]
            await self.socket_service.send_message_to_room(message, room_id=0)
        except Exception as e:
            logger.error(f'Error notifying clients about rooms: {e}')
            raise
