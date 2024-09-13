from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from db.models.user import User
from repositories.user_repository import UserRepository
from repositories.user_room_repository import UserRoomRepository
from services.auth_services import AuthService
from services.room_service import RoomManagerService
from services.socket_service import ConnectionManager
from services.user_services import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    """
    Dependency function to get an instance of UserRepository.

    Args:
        session (AsyncSession): The database session.

    Returns:
        UserRepository: An instance of UserRepository.
    """
    return UserRepository(session=session)


async def get_user_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserService:
    """
    Dependency function to get an instance of UserService.

    Args:
        user_repo (UserRepository): An instance of UserRepository.

    Returns:
        UserService: An instance of UserService.
    """
    return UserService(user_repo=user_repo)


async def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    """
    Dependency function to get an instance of AuthService.

    Args:
        user_repo (UserRepository): An instance of UserRepository.

    Returns:
        AuthService: An instance of AuthService.
    """
    return AuthService(user_repo=user_repo)


async def get_current_user(
    auth_service: AuthService = Depends(get_auth_service), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependency function to get the currently authenticated user.

    Args:
        auth_service (AuthService): An instance of AuthService.
        token (str): The OAuth2 token.

    Returns:
        User: The currently authenticated user.
    """
    return await auth_service.get_current_user_from_token(token=token)


def get_connection_manager() -> ConnectionManager:
    """
    Dependency function to get an instance of ConnectionManager.

    Returns:
        ConnectionManager: An instance of ConnectionManager.
    """
    return ConnectionManager()


async def get_user_room_repository(db: AsyncSession = Depends(get_db)) -> UserRoomRepository:
    """
    Dependency function to get an instance of UserRoomRepository.

    Args:
        db (AsyncSession): The database session.

    Returns:
        UserRoomRepository: An instance of UserRoomRepository.
    """
    return UserRoomRepository(db)


async def get_room_manager_service(
    room_repo: UserRoomRepository = Depends(get_user_room_repository),
    connection_manager: ConnectionManager = Depends(get_connection_manager),
) -> RoomManagerService:
    """
    Dependency function to get an instance of RoomManagerService.

    Args:
        room_repo (UserRoomRepository): An instance of UserRoomRepository.
        connection_manager (ConnectionManager): An instance of ConnectionManager.

    Returns:
        RoomManagerService: An instance of RoomManagerService.
    """
    return RoomManagerService(room_repo=room_repo, socket_service=connection_manager)
