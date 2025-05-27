from typing import List
from uuid import UUID
from app.infraestructure.db.repository import create_tags, get_tags_list
from app.api.schemas import Tag
from sqlalchemy.ext.asyncio import AsyncSession

async def create_tags_use_case(db: AsyncSession, tags:List[Tag], user_id):

    return await create_tags(db,tags, user_id)


async def get_tags(db:AsyncSession, user_id:UUID):

    return await get_tags_list(db, user_id)