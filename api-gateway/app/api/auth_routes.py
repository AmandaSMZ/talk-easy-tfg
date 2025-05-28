from fastapi import APIRouter, Depends, Request
from app.dependencies import get_current_user
from app.proxy import proxy_request
from config import settings
from app.api.schemas import UserCredentials
from app.api.utils import user_headers

router = APIRouter()


@router.post("/auth/login")
async def login(request: UserCredentials):
    return await proxy_request(base_url=settings.AUTH_API_URL, method="POST", endpoint="auth/login", expected_status_code=200, body=request.model_dump())

@router.post("/auth/register")
async def register(request: UserCredentials):
    return await proxy_request(base_url=settings.AUTH_API_URL, method="POST", endpoint="auth/register", expected_status_code=201, body=request.model_dump())

@router.get("/auth/me")
async def me(user=Depends(get_current_user)):
    headers = user_headers(user)
    return await proxy_request(base_url=settings.AUTH_API_URL, method="GET", endpoint="auth/me", expected_status_code=200, headers=headers)
