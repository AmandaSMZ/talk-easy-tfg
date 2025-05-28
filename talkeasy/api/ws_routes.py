from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from infraestructure.websockets.connection_manager import connection_manager


ws_router = APIRouter()

@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    user_id_str = websocket.query_params.get('user_id')

    try:
        user_id = UUID(user_id_str)
    except ValueError:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    await connection_manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.disconnect(user_id)
