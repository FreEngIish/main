from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from db.models.user import User
from repositories.user_repository import UserRepository
from repositories.user_room_repository import UserRoomRepository
from services.auth_services import AuthService
from services.connection_service import ConnectionManager
from services.room_service import RoomManagerService
from services.user_services import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(session=session)


def get_user_room_repository(session: AsyncSession = Depends(get_db)) -> UserRoomRepository:
    return UserRoomRepository(session=session)


def get_connection_manager() -> ConnectionManager:
    return ConnectionManager()


async def get_user_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repo=user_repo)


async def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repo=user_repo)


async def get_current_user(
        auth_service: AuthService = Depends(get_auth_service),
        token: str = Query(None)
) -> User:
    return await auth_service.get_current_user_from_token(token=token)



async def get_room_manager_service(
        room_repo: UserRoomRepository = Depends(get_user_room_repository),
        connection_manager: ConnectionManager = Depends(get_connection_manager),
        db: AsyncSession = Depends(get_db)
) -> RoomManagerService:
    return RoomManagerService(room_repo=room_repo, socket_service=connection_manager, db=db)
