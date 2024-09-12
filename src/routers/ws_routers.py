import json

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from db import User
from db.database import get_db
from dependencies import get_current_user
from repositories.user_room_repository import UserRoomRepository
from schemas.user_room_schemas import UserRoomResponseSchema
from websocket.connection_manager import ConnectionManager


router = APIRouter()

manager = ConnectionManager()


@router.websocket("/ws/rooms")
async def websocket_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    room_repo = UserRoomRepository(db)

    await manager.connect(websocket, room_id=0)
    try:
        # Получаем все комнаты из базы данных
        rooms = await room_repo.get_all_rooms()

        rooms_data = [UserRoomResponseSchema.from_orm(room) for room in rooms]

        rooms_json = [room.json() for room in rooms_data]

        # Отправляем данные клиенту
        await websocket.send_text(f"[{','.join(rooms_json)}]")

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id=0)


async def notify_all_clients_about_rooms(db: AsyncSession):
    room_repo = UserRoomRepository(db)
    rooms = await room_repo.get_all_rooms()

    rooms_data = [UserRoomResponseSchema.from_orm(room) for room in rooms]

    message = [room.json() for room in rooms_data]

    await manager.send_message_to_room(message, room_id=0)


@router.post("/rooms/")
async def create_room(
        name: str,
        native_language: str,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """POST-запрос для создания новой комнаты с creator_id из JWT"""
    room_repo = UserRoomRepository(db)
    new_room = await room_repo.create_room(
        room_name=name,
        creator_id=current_user.id,
        native_language=native_language
    )

    await notify_all_clients_about_rooms(db)

    return new_room
