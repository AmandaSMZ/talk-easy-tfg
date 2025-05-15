from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from infraestructure.websockets.connection_manager import connection_manager

ws_router = APIRouter()

@ws_router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await connection_manager.connect(username, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            
    except WebSocketDisconnect:
        connection_manager.disconnect(username)