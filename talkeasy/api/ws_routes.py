from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from infraestructure.websockets.connection_manager import connection_manager
from infraestructure.auth.dependencies import MESSAGE_FORBIDDEN, verify_ws_token

ws_router = APIRouter()

@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    secret = websocket.query_params.get("token")
    user_id_str: str = websocket.query_params.get('user_id')

    try:
        user_id = UUID(user_id_str)
    except Exception:
        await websocket.close(code=1008)
        return
    
    if not secret or not verify_ws_token(secret):
        await websocket.close(code=1008)
        return
    
    try:
        user_id = UUID(user_id_str)
    except Exception:
        await websocket.close(code=1008)
        return
    
    await websocket.accept()
    await connection_manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
            connection_manager.disconnect(user_id)