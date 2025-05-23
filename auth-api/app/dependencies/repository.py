from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.data.db.repository import UserRepository
from app.data.db.db import get_db

def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)