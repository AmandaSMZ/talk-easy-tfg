from typing import List
from fastapi import APIRouter, Depends, status
from app.dependencies import get_current_user
from app.proxy import proxy_request
from config import settings
from app.api.schemas.user_schemas import UserCredentials, UserCreate, UserRead, Token, UserSearch
from app.api.utils import user_headers

router = APIRouter()


@router.post("/auth/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(request: UserCredentials):
    return await proxy_request(base_url=settings.AUTH_API_URL, method="POST", endpoint="auth/login", expected_status_code=200, body=request.model_dump())

@router.post("/auth/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(request: UserCreate):
    return await proxy_request(base_url=settings.AUTH_API_URL, method="POST", endpoint="auth/register", expected_status_code=201, body=request.model_dump())

@router.get("/auth/me", status_code=status.HTTP_200_OK)
async def me(user=Depends(get_current_user)):
    headers = user_headers(user)
    return await proxy_request(base_url=settings.AUTH_API_URL, method="GET", endpoint="auth/me", expected_status_code=200, headers=headers)

@router.get("/search/{email:path}", status_code=status.HTTP_200_OK, response_model=List[UserSearch])
async def search_users_route(
    email: str,
    user = Depends(get_current_user)
):
    headers = user_headers(user)
    endpoint= f'/auth/search/{email}'

    return await proxy_request(base_url=settings.AUTH_API_URL, method="GET", endpoint=endpoint, expected_status_code=200, headers=headers)