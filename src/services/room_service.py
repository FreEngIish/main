from typing import List

from fastapi import WebSocket, WebSocketDisconnect

from db.models.user import User
from db.models.user_room import UserRoom
from repositories.user_room_repository import UserRoomRepository
from schemas.user_room_schemas import UserRoomCreateSchema, UserRoomResponseSchema
from services.connection_service import ConnectionManager


class RoomManagerService:
    def __init__(self, room_repo: UserRoomRepository, socket_service: ConnectionManager):
        self.room_repo = room_repo
        self.socket_service = socket_service

    async def handle_main_page_connection(self, websocket: WebSocket, current_user: User):
        await self.socket_service.connect(websocket)

        try:
            rooms: List[UserRoom] = await self.get_all_rooms()
            rooms_json = [UserRoomResponseSchema.from_orm(room).dict() for room in rooms]
            await websocket.send_json(rooms_json)

            while True:
                data = await websocket.receive_json()

                if "create_room" in data:
                    room_data = UserRoomCreateSchema(**data["create_room"])
                    created_room = await self.create_room(room_data, current_user)
                    await self.broadcast_rooms()

        except WebSocketDisconnect:
            await self.socket_service.disconnect(websocket)

    async def create_room(self, room_data: UserRoomCreateSchema, current_user: User) -> UserRoom:
        new_room = UserRoom(
            room_name=room_data.room_name,
            native_language=room_data.native_language,
            language_level=room_data.language_level,
            participant_limit=room_data.participant_limit,
            creator_id=current_user.id
        )
        return await self.room_repo.add_room(new_room)

    async def get_all_rooms(self) -> List[UserRoom]:
        return await self.room_repo.get_all_rooms()

    async def broadcast_rooms(self):
        rooms: List[UserRoom] = await self.get_all_rooms()
        rooms_json = [UserRoomResponseSchema.from_orm(room).dict() for room in rooms]
        await self.socket_service.broadcast_json(rooms_json)
