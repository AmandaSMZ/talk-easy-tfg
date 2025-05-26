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








