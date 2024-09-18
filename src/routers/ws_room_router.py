from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from dependencies import get_room_manager_service
from services.room_service import RoomManagerService


router = APIRouter()


@router.websocket("/ws/rooms")
async def websocket_endpoint(
        websocket: WebSocket,
        room_service: RoomManagerService = Depends(get_room_manager_service)
):
    try:
        await room_service.handle_main_page_connection(websocket, current_user=None)
    except WebSocketDisconnect:
        print("Client disconnected")
