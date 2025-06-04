from typing import List
from uuid import UUID
from app.infraestructure.db.repository import create_tags, get_tag_by_names, get_tag_list, delete_tag
from app.api.schemas import Tag
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.service import classifier_service

async def create_tags_use_case(db: AsyncSession, tags:List[Tag], user_id):

    return await create_tags(db,tags, user_id)

async def delete_tag_use_case(db:AsyncSession, tag_id:UUID, user_id:UUID):
    return await delete_tag(db,tag_id,user_id)

async def get_tags(db:AsyncSession, user_id:UUID):

    return await get_tag_list(db, user_id)

async def get_message_tags(db:AsyncSession, user_id:UUID, text:str) -> List[Tag]:

    user_tags = await get_tags(db, user_id)
    user_tag_names = [tag.name for tag in user_tags]

    if user_tag_names:
        response = classifier_service.tag_message(text=text, tags=user_tag_names)
        if response:
            return await get_tag_by_names(db, response)
        
    return []
    