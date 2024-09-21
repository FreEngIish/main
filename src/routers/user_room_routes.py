from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from dependencies import get_current_user
from repositories.user_room_repository import UserRoomRepository
from schemas.user_room_schemas import UserRoomCreateSchema, UserRoomResponseSchema, UserRoomUpdateSchema
from services.user_room_service import UserRoomService


router = APIRouter()

@router.post('/rooms/', response_model=UserRoomResponseSchema)
async def create_room(
    room_data: UserRoomCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    user_room_repo = UserRoomRepository(db)
    service = UserRoomService(user_room_repo)
    new_room = await service.create_room(room_data, current_user)
    return new_room

@router.get('/rooms/{room_id}', response_model=UserRoomResponseSchema)
async def get_room(room_id: int, db: AsyncSession = Depends(get_db)):
    user_room_repo = UserRoomRepository(db)
    service = UserRoomService(user_room_repo)
    room = await service.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail='Room not found')
    return room

@router.put('/rooms/{room_id}', response_model=UserRoomResponseSchema)
async def update_room(
    room_id: int,
    room_data: UserRoomUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    user_room_repo = UserRoomRepository(db)
    service = UserRoomService(user_room_repo)
    updated_room = await service.update_room(room_id, room_data, current_user)
    if not update_room:
        raise HTTPException(status_code=404, detail='Room not found or permission denied')
    return updated_room

@router.patch('/rooms/{room_id}', response_model=UserRoomResponseSchema)
async def partial_update_room(
    room_id: int,
    room_data: UserRoomUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    user_room_repo = UserRoomRepository(db)
    service = UserRoomService(user_room_repo)
    updated_room = await service.update_room(room_id, room_data, current_user)
    if not updated_room:
        raise HTTPException(status_code=404, detail='Room not found or permission denied')
    return updated_room
