from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv
from app.proxy import proxy_request

load_dotenv()

AUTH_API_URL = os.getenv('AUTH_API_URL')
TALKEASY_API_URL = os.getenv('TALKEASY_API_URL')

app = FastAPI(title="API Gateway", version="1.0")

@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def auth_proxy(request: Request, path: str):
    return await proxy_request(request, base_url=AUTH_API_URL)

@app.api_route("/messages/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def messages_proxy(request: Request, path: str):
    return await proxy_request(request, base_url=TALKEASY_API_URL)


