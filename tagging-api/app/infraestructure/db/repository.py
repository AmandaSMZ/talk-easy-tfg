from typing import List
from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.db.models import TagModel
from app.api.schemas import TagOut, TagIn, Tag


async def create_tags(db: AsyncSession, tags: List[str], user_id:UUID):

    saved_tags = []
    for tag in tags:
        name = tag.name.strip()

        if not name:
            continue

        existing_tag_result = await db.execute(
            select(TagModel).where(
                TagModel.name == name,
                TagModel.user_id == user_id
            )
        )

        existing_tag = existing_tag_result.scalars().first()

        if existing_tag:
            saved_tags.append(existing_tag)

        else:
            new_tag = TagModel(name=name, user_id=user_id)
            db.add(new_tag)
            await db.commit()
            await db.refresh(new_tag)
            saved_tags.append(new_tag)

    return [Tag(id=tag.id, name=tag.name) for tag in saved_tags]

async def get_tags_list(db: AsyncSession, user_id:UUID):
    result = await db.execute(select(TagModel).where(TagModel.user_id==user_id))
    tags_objs = result.scalars().all()
    return [TagOut(id=tag.id) for tag in tags_objs]

async def get_name_tags_from_ids(db:AsyncSession, tag_ids:list[UUID]) -> list[str]:
    if not tag_ids:
        return []
    result = await db.execute(select(TagModel).where(TagModel.id.in_(tag_ids)))
    tags = result.scalars().all()
    return [TagIn(name=tag.name) for tag in tags]


async def get_tag_ids_by_names(db: AsyncSession, tag_names: list[str]) -> list[UUID]:

    result = await db.execute(select(TagModel).where(TagModel.name.in_(tag_names)))
    tag_objs = result.scalars().all()
    return [tag.id for tag in tag_objs]