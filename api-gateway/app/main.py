from fastapi import Depends, FastAPI, HTTPException, Request
import os
from dotenv import load_dotenv
import httpx
from pydantic import BaseModel
from app.proxy import INTERNAL_TOKEN, proxy_request
from fastapi import WebSocket, WebSocketDisconnect
import websockets
import asyncio
from services.auth_token import get_current_user
from service import TALKEASY_API_URL, get_available_tags, request_tags

load_dotenv()

AUTH_API_URL = "http://auth-api:8000/auth/me"
MESSAGES_API_URL = "http://talkeasy-api:8002"
INTERNAL_SECRET = "tu_token_super_secreto"

app = FastAPI(title="API Gateway", version="1.0")

@app.websocket("/talk")
async def talk_to_talkeasy(
    client_ws: WebSocket,
    user = Depends(get_current_user)
):
    await client_ws.accept()
    user_id = str(user["id"])
    talkeasy_url = (
      f"ws://talk_easy:8000/ws"
      f"?token={INTERNAL_SECRET}"
      f"&user_id={user_id}"
    )
    try:
        async with ws_connect(talkeasy_url) as srv_ws:
            # Bucle único: del microservicio → al cliente
            while True:
                msg = await srv_ws.recv()         # recibe de TalkEasy
                await client_ws.send_text(msg)    # envía al cliente
    except WebSocketDisconnect:
        pass
    finally:
        await client_ws.close()

'''
@app.api_route("/messages/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def messages_proxy(request: Request, path: str, user = Depends(get_current_user)):
    return await proxy_request(request, base_url=MESSAGES_API_URL, user=user)
'''






