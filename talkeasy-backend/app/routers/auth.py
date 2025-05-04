from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from use_cases.auth.authenticate_user import authenticate_user
from domain.schemas.auth_schema import LoginRequest, TokenResponse
from infraestructure.postgres.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await authenticate_user(db, credentials)