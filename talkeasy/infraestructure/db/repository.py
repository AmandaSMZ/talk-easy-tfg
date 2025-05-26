from typing import List, Optional
from uuid import UUID
from sqlalchemy import and_, or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.message_domain import DomainTag
from infraestructure.db.models import MessageModel, MessageTagModel, TagsModel
from mappers import db_message_to_domain, db_tag_to_domain_tag, domain_message_to_db_model, domain_tag_to_db_model

async def save_new_message(db: AsyncSession, domain_msg):

    db_msg = domain_message_to_db_model(domain_msg)

    db.add(db_msg)
    await db.commit()
    await db.refresh(db_msg)

    domain_tags_id = domain_msg.tags or []
    if domain_tags_id:
        await update_message_tags(db, db_msg.id, domain_tags_id)

    result = await db.execute(select(TagsModel).where(TagsModel.id.in_(domain_msg.tags or [])))
    tags = result.scalars().all()

    return db_message_to_domain(db_msg,tags)
    

async def update_message_tags(db: AsyncSession, msg_id:UUID, tags: list[UUID]):

    tag_objs = [
        MessageTagModel(message_id=msg_id, tag_id=tag_id) 
        for tag_id in tags
        ]
    
    db.add_all(tag_objs)
    await db.commit()


async def get_chat_messages(db: AsyncSession, user1: UUID, user2: UUID, last_id: Optional[UUID] = None):

    stmt = select(MessageModel).where(
        or_(
            and_(MessageModel.from_user_id == user1, MessageModel.to_user_id == user2),
            and_(MessageModel.from_user_id == user2, MessageModel.to_user_id == user1)
        )
    )
    if last_id:
        stmt = stmt.where(MessageModel.id > last_id)
    stmt = stmt.order_by(MessageModel.timestamp)

    res = await db.execute(stmt)
    messages = res.scalars().all()

    result = []

    for msg in messages:

        tag_rel_result = await db.execute(select(MessageTagModel.tag_id).where(MessageTagModel.message_id == msg.id))
        tag_ids = tag_rel_result.scalars().all()
        print(tag_ids)
        tags = []

        if tag_ids:
            tag_result = await db.execute(select(TagsModel).where(TagsModel.id.in_(tag_ids)))
            tags = tag_result.scalars().all()

        domain_msg = db_message_to_domain(msg, tags)
        result.append(domain_msg)

    return result


async def create_tags(db: AsyncSession, tags: List[DomainTag]):

    saved_tags = []
    for tag in tags:
        name = tag.name.strip()

        if not name:
            continue

        existing_tag_result = await db.execute(select(TagsModel).where(TagsModel.name == name))
        existing_tag = existing_tag_result.scalars().first()

        if existing_tag:
            saved_tags.append(existing_tag)

        else:
            new_tag = TagsModel(name=name)
            db.add(new_tag)
            await db.commit()
            await db.refresh(new_tag)
            saved_tags.append(new_tag)

    return [domain_tag_to_db_model(tag) for tag in saved_tags]

async def get_tags_list(db: AsyncSession):
    result = await db.execute(select(TagsModel))
    tags_objs = result.scalars().all()
    return [db_tag_to_domain_tag(tag) for tag in tags_objs]

async def get_name_tags_from_ids(db:AsyncSession, tag_ids:list[UUID]) -> list[str]:
    if not tag_ids:
        return []
    result = await db.execute(select(TagsModel).where(TagsModel.id.in_(tag_ids)))
    tags = result.scalars().all()
    return [tag.name for tag in tags]


async def get_tag_ids_by_names(db: AsyncSession, tag_names: list[str]) -> list[UUID]:
    result = await db.execute(select(TagsModel).where(TagsModel.name.in_(tag_names)))
    tag_objs = result.scalars().all()
    return [tag.id for tag in tag_objs]