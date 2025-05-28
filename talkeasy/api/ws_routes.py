from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from infraestructure.websockets.connection_manager import connection_manager


ws_router = APIRouter()

@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    token = websocket.query_params.get('token')

    if token is None:
        await websocket.close(code=1008)
        return
    

    user = decode_token_and_get_user(token)
    
    if user is None:
        await websocket.close(code=1008)
        return
    
    user_id = user['id']

    await websocket.accept()
    await connection_manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.disconnect(user_id)


    user_id_str: str = websocket.query_params.get('user_id')

    try:
        user_id = UUID(user_id_str)
    except Exception:
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