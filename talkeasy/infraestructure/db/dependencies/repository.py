from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infraestructure.db.repository.message_repository import SQLAlchemyMessageRepository
from infraestructure.db.dependencies.db import get_db


async def get_message_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyMessageRepository:
    return SQLAlchemyMessageRepository(db)