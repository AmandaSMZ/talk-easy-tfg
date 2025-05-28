from fastapi import WebSocket, HTTPException, status
from fastapi.websockets import WebSocketState
from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.dependencies import decode_token_and_get_user


ws_router = APIRouter()

@ws_router.websocket("/ws")
async def websocket_proxy(websocket: WebSocket):
    await websocket.accept()

    token = websocket.query_params.get('token')
    if not token:
        await websocket.close(code=1008)
        return

    try:
        user_data = decode_token_and_get_user(token)
        user_id = user_data['user_id']
    except HTTPException:
        await websocket.close(code=1008)
        return

    backend_ws_url = f"ws://talkeasy-api:8000/ws?user_id={user_id}"

    try:
        import websockets

        async with websockets.connect(backend_ws_url) as backend_ws:

            async def send_to_client():
                while True:
                    msg = await backend_ws.recv()
                    if websocket.application_state == WebSocketState.CONNECTED:
                        await websocket.send_text(msg)
                    else:
                        break

            await send_to_client()

    except Exception:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)