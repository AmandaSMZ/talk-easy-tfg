from sqlalchemy.ext.asyncio import AsyncSession
from infraestructure.postgres.models.user_model import User
from infraestructure.auth import security
from domain.schemas.auth_schema import UserCreate, UserLogin, Token
from fastapi import HTTPException
from sqlalchemy.future import select

async def register_user(data: UserCreate, db: AsyncSession) -> Token:
    result = await db.execute(select(User).where(User.email == data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    user = User(
        email=data.email,
        hashed_password=security.hash_password(data.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return await login_user(UserLogin(email=data.email, password=data.password), db)

async def login_user(data: UserLogin, db: AsyncSession) -> Token:
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user or not security.verify_password(data.password, user.hashed_password):
        raise HTTPException(401, detail="Credenciales inválidas")

    access_token = security.create_access_token({"sub": str(user.id)})
    refresh_token = security.create_refresh_token({"sub": str(user.id)})
    user.refresh_token = refresh_token
    await db.commit()
    return Token(access_token=access_token, refresh_token=refresh_token)

async def refresh_tokens(refresh_token: str, db: AsyncSession) -> Token:
    try:
        payload = security.decode_token(refresh_token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(403, detail="Token inválido")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or user.refresh_token != refresh_token:
        raise HTTPException(403, detail="Refresh token no válido")

    new_access = security.create_access_token({"sub": str(user.id)})
    new_refresh = security.create_refresh_token({"sub": str(user.id)})
    user.refresh_token = new_refresh
    await db.flush()
    await db.commit()
    return Token(access_token=new_access, refresh_token=new_refresh)
