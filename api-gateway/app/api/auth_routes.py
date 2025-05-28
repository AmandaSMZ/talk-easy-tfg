from fastapi import APIRouter, Depends, Request
from app.dependencies import get_current_user
from app.proxy import proxy_request
from config import settings

router = APIRouter()


@router.post("/auth/login")
async def login(request: Request):
    body = await request.json()
    return await proxy_request(base_url=settings.AUTH_API_URL, method="POST", endpoint="auth/login", expected_status_code=200, body=body)

@router.post("/auth/register")
async def register(request: Request):
    body = await request.json()
    return await proxy_request(base_url=settings.AUTH_API_URL, method="POST", endpoint="auth/register", expected_status_code=201, body=body)

@router.get("/auth/me")
async def me(user=Depends(get_current_user)):
    headers = {"X-User-Id": user["user_id"]}
    return await proxy_request(base_url=settings.AUTH_API_URL, method="GET", endpoint="auth/me", expected_status_code=200)
