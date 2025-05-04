# app/infrastructure/postgres/repositories/user_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from infraestructure.postgres.models.user_model import User
from domain.schemas.auth_schema import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(db: AsyncSession, user: UserCreate):
    hashed_pw = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User).where(User.email == email))
    
    return result.scalars().first()
