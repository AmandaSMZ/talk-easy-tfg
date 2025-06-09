from typing import List
from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.db.models import TagModel
from app.api.schemas import TagIn, Tag


async def create_tags(db: AsyncSession, 
                      tag: TagIn, 
                      user_id: UUID):

    name = tag.name.strip().upper()
    if not name:
        return None

    result = await db.execute(
        select(TagModel).where(
            TagModel.name == name,
            TagModel.user_id == user_id
            )
        )
    tag_model = result.scalars().first()

    if tag_model:
        if not tag_model.active:
            tag_model.active = True
            await db.commit()
            await db.refresh(tag_model)
            return tag_model
        else:
            # Si la etiqueta ya existe y está activa, no se hace nada
            return None

    # Si no existe, se crea una nueva
    new_tag = TagModel(name=name, user_id=user_id)
    db.add(new_tag)
    await db.commit()
    await db.refresh(new_tag)

    return new_tag


async def deactivate_tag(db: AsyncSession, tag_id: UUID, user_id: UUID):
    result = await db.execute(
        select(TagModel).where(
            TagModel.id == tag_id,
            TagModel.user_id == user_id
        )
    )
    tag = result.scalar_one_or_none()

    if not tag:
        return False

    tag.active = False
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return True

async def get_all_tag_list(db: AsyncSession,
                              user_id: UUID):
    result = await db.execute(
        select(TagModel)
            .where(TagModel.user_id == user_id))
    tags_objs = result.scalars().all()
    return [Tag(name=tag.name, id=str(tag.id)) for tag in tags_objs]

async def get_active_tag_list(db: AsyncSession,
                              user_id: UUID):
    result = await db.execute(
        select(TagModel)
            .where(TagModel.user_id == user_id,
                    TagModel.active == True))
    
    tags_objs = result.scalars().all()
    return [Tag(name=tag.name, id=str(tag.id)) for tag in tags_objs]


async def get_name_tags_from_ids(db:AsyncSession, tag_ids:list[UUID]) -> list[str]:
    if not tag_ids:
        return []
    result = await db.execute(select(TagModel).where(TagModel.id.in_(tag_ids)))
    tags = result.scalars().all()
    return [tag.name for tag in tags]



async def get_tag_by_names(db: AsyncSession, tag_names: list[str], user_id: UUID) -> list[Tag]:

    result = await db.execute(select(TagModel).where(TagModel.name.in_(tag_names), TagModel.user_id == user_id))
    tag_objs = result.scalars().all()
    return [Tag(id=str(tag.id), name=tag.name) for tag in tag_objs]