from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user_repository import UserRepository
from repositories.user_room_repository import UserRoomRepository
from schemas.user_room_schemas import UserRoomResponseSchema
from services.auth_services import AuthService
from websocket.connection_manager import ConnectionManager


manager = ConnectionManager()


async def notify_all_clients_about_rooms(db: AsyncSession):
    room_repo = UserRoomRepository(db)
    rooms = await room_repo.get_all_rooms()

    rooms_data = [UserRoomResponseSchema.from_orm(room) for room in rooms]

    message = [room.json() for room in rooms_data]

    await manager.send_message_to_room(message, room_id=0)


async def get_current_user_ws(token: str, db: AsyncSession):
    """Получение текущего пользователя из JWT токена для вебсокета."""
    auth_service = AuthService(UserRepository(db))
    try:
        user = await auth_service.get_current_user_from_token(token)
        return user
    except JWTError:
        return None
