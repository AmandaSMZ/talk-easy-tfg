from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from app.websockets.connection_manager import connection_manager
from app.dependencies import decode_token_and_get_user

ws_router = APIRouter()

@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        user = decode_token_and_get_user(token)
        user_id = UUID(user["user_id"])
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    await connection_manager.connect(user_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.disconnect(user_id)
