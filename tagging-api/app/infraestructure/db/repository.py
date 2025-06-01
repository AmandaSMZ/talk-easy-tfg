from typing import List
from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.db.models import TagModel
from app.api.schemas import TagIn, Tag


async def create_tags(db: AsyncSession, tags: List[TagIn], user_id:UUID):
    created_new = False

    for tag in tags:
        name = tag.name.strip()
        if not name:
            continue

        result = await db.execute(
            select(TagModel).where(
                TagModel.name == name,
                TagModel.user_id == user_id
            )
        )
        tag_model = result.scalars().first()

        if not tag_model:
            new_tag = TagModel(name=name, user_id=user_id)
            db.add(new_tag)
            await db.commit()
            await db.refresh(new_tag)
            created_new = True

    return created_new

async def delete_tag(db: AsyncSession, tag_id: UUID, user_id: UUID):
    result = await db.execute(
        select(TagModel).where(TagModel.id == tag_id, TagModel.user_id == user_id)
    )
    tag = result.scalar_one_or_none()
    if not tag:
        return False

    await db.delete(tag)
    await db.commit()
    return True


async def get_tag_list(db:AsyncSession, user_id:UUID):
    result = await db.execute(select(TagModel).where(TagModel.user_id==user_id))
    tags_objs = result.scalars().all()
    return [Tag(name=tag.name, id=str(tag.id)) for tag in tags_objs]

async def get_name_tags_from_ids(db:AsyncSession, tag_ids:list[UUID]) -> list[str]:
    if not tag_ids:
        return []
    result = await db.execute(select(TagModel).where(TagModel.id.in_(tag_ids)))
    tags = result.scalars().all()
    return [tag.name for tag in tags]


async def get_tag_by_names(db: AsyncSession, tag_names: list[str]) -> list[Tag]:

    result = await db.execute(select(TagModel).where(TagModel.name.in_(tag_names)))
    tag_objs = result.scalars().all()
    return [Tag(id=str(tag.id), name=tag.name) for tag in tag_objs]