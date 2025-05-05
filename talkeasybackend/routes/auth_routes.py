from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from domain.schemas.auth_schema import UserCreate, UserLogin, Token
from domain.use_cases import auth
from infraestructure.postgres.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await auth.register_user(data, db)

@router.post("/login", response_model=Token)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await auth.login_user(data, db)

@router.post("/refresh", response_model=Token)
async def refresh(refresh_token: str, db: AsyncSession = Depends(get_db)):
    return await auth.refresh_tokens(refresh_token, db)

@router.post("/logout")
async def logout(refresh_token: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.refresh_token == refresh_token))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=403, detail="Refresh token no válido")
    
    user.refresh_token = None
    await db.commit()
    return {"message": "Logout exitoso"}


from sqlalchemy.future import select
from fastapi import HTTPException
from infraestructure.postgres.models.user_model import User