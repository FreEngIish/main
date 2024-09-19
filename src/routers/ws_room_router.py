from datetime import datetime

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from repositories.message_repository import MessageRepository
from repositories.user_repository import UserRepository
from repositories.user_room_repository import UserRoomRepository
from schemas.message_schemas import MessageCreateSchema, MessageResponseSchema
from services.auth_services import AuthService
from services.websocket_services import manager


router = APIRouter()


async def get_current_user_ws(token: str, db: AsyncSession):
    """Getting current user from JWT token for websocket."""
    auth_service = AuthService(UserRepository(db))
    try:
        user = await auth_service.get_current_user_from_token(token)
        return user
    except JWTError:
        return None


@router.websocket("/ws/room/{room_id}")
async def websocket_room_connection(
        websocket: WebSocket,
        room_id: int,
        token: str = Query(...),
        db: AsyncSession = Depends(get_db)
):
    current_user = await get_current_user_ws(token, db)

    if current_user is None:
        await websocket.close(code=1008)
        return

    room_repo = UserRoomRepository(db)
    message_repo = MessageRepository(db)

    await manager.connect(websocket, room_id)
    try:
        room = await room_repo.get_room(room_id)
        if not room:
            await websocket.send_text(f"Room with ID {room_id} does not exist.")
            return

        messages = await message_repo.get_messages_by_room(room_id)
        for message in messages:
            message_data = MessageResponseSchema.from_orm(message).json()
            await websocket.send_text(message_data)

        while True:
            data = await websocket.receive_text()
            message_create = MessageCreateSchema(room_id=room_id, message_text=data)

            new_message = await message_repo.create_message(room_id, current_user.id, message_create.message_text)

            message_response = MessageResponseSchema(
                message_id=new_message.message_id,
                room_id=new_message.room_id,
                user_id=new_message.user_id,
                message_text=new_message.message_text,
                timestamp=datetime.now()
            )
            await manager.send_message_to_room(message_response.json(), room_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)