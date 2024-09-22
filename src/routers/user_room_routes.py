from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_current_user, get_user_room_service
from exceptions import PermissionDeniedException, RoomNotFoundException
from schemas.user_room_schemas import UserRoomCreateSchema, UserRoomResponseSchema, UserRoomUpdateSchema
from services.user_room_service import UserRoomService


router = APIRouter(tags=['UserRoom'])

@router.post('/rooms/', response_model=UserRoomResponseSchema)
async def create_room(
    room_data: UserRoomCreateSchema,
    current_user: int = Depends(get_current_user),
    service: UserRoomService = Depends(get_user_room_service)
):
    new_room = await service.create_room(room_data, current_user)
    return new_room

@router.get('/rooms/{room_id}', response_model=UserRoomResponseSchema)
async def get_room(
    room_id: int,
    service: UserRoomService = Depends(get_user_room_service)
):
    try:
        room = await service.get_room(room_id)
        return room
    except RoomNotFoundException:
        raise HTTPException(status_code=404, detail='Room not found')

@router.put('/rooms/{room_id}', response_model=UserRoomResponseSchema)
async def update_room(
    room_id: int,
    room_data: UserRoomUpdateSchema,
    current_user: int = Depends(get_current_user),
    service: UserRoomService = Depends(get_user_room_service)
):
    try:
        updated_room = await service.update_room(room_id, room_data, current_user)
        return updated_room
    except RoomNotFoundException:
        raise HTTPException(status_code=404, detail='Room not found')
    except PermissionDeniedException:
        raise HTTPException(status_code=403, detail='Permission denied')

@router.patch('/rooms/{room_id}', response_model=UserRoomResponseSchema)
async def partial_update_room(
    room_id: int,
    room_data: UserRoomUpdateSchema,
    current_user: int = Depends(get_current_user),
    service: UserRoomService = Depends(get_user_room_service)
):
    try:
        updated_room = await service.update_room(room_id, room_data, current_user)
        return updated_room
    except RoomNotFoundException:
        raise HTTPException(status_code=404, detail='Room not found')
    except PermissionDeniedException:
        raise HTTPException(status_code=403, detail='Permission denied')
