from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from starlette import status

from db import User
from dependencies import get_current_user, get_room_service
from schemas.user_room_schemas import UserRoomCreateSchema
from services.room_service import RoomService


router = APIRouter()


@router.websocket('/ws/rooms')
async def websocket_endpoint(websocket: WebSocket, room_service: RoomService = Depends(get_room_service)):
    """
    WebSocket endpoint to handle room updates and communicate with clients.

    Args:
        websocket (WebSocket): The WebSocket connection instance.
        room_service (RoomService): An instance of RoomService for room operations.

    This endpoint:
    - Accepts a WebSocket connection.
    - Sends a list of all rooms in JSON format to the connected client.
    - Keeps the connection open and waits for messages from the client.
    - Disconnects and cleans up when the WebSocket connection is closed.
    """
    await room_service.socket_service.connect(websocket, room_id=0)
    try:
        rooms_data = await room_service.get_all_rooms()
        rooms_json = [room.json() for room in rooms_data]
        await websocket.send_text(f"[{','.join(rooms_json)}]")

        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await room_service.socket_service.disconnect(websocket, room_id=0)


@router.post('/rooms/', response_model=UserRoomCreateSchema, status_code=status.HTTP_201_CREATED)
async def create_room(
    room_create_request: UserRoomCreateSchema,
    room_service: RoomService = Depends(get_room_service),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new room and notify all connected clients about the update.

    Args:
        room_create_request (UserRoomCreateSchema): The details of the room to be created.
        room_service (RoomService): An instance of RoomService for room operations.
        current_user (User): The currently authenticated user creating the room.

    Returns:
        UserRoomCreateSchema: The newly created room object.

    Raises:
        HTTPException:
            - If room creation fails or other issues occur.
            - If the user is not authenticated.
            - If invalid input is provided.
    """
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found or not authenticated')

    if not room_create_request.room_name or not room_create_request.native_language:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input: Both 'name' and 'native_language' are required.",
        )

    try:
        new_room = await room_service.create_room(room_request=room_create_request, creator=current_user)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='An error occurred while creating the room'
        )
    return new_room
