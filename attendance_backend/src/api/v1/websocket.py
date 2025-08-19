from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Set
from src.services.users_service import UsersService

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: str):
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except RuntimeError:
                self.disconnect(connection)

manager = ConnectionManager()

# PUBLIC_INTERFACE
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user=Depends(UsersService.get_current_user_ws)):
    """
    WebSocket channel for real-time attendance updates.
    Requires a valid Authorization header with a Bearer token.
    Sends and receives ping/pong to keep connection alive.
    """
    await manager.connect(websocket)
    try:
        while True:
            msg = await websocket.receive_text()
            if msg.lower() == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
