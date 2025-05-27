from typing import List, Optional
from uuid import UUID
from sqlalchemy import and_, or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.message_domain import DomainConversation
from infraestructure.db.models import Conversation, MessageModel, MessageTagModel, TagsModel
from mappers import db_message_to_domain, domain_message_to_db_model

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

        subq = (
      select(MessageModel.timestamp)
      .where(MessageModel.id == last_id)
      .scalar_subquery()
    )
        stmt = stmt.where(MessageModel.timestamp > subq)

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


async def create_conversation_if_not_exists(db, user1: UUID, user2: UUID) -> None:

        u1, u2 = sorted([user1, user2], key=str)

        conv = Conversation(user1_id=u1, user2_id=u2)

        await db.merge(conv)

        await db.commit()

async def list_interlocutors(db, me: UUID) -> List[UUID]:

    stmt = select(Conversation).where(
            or_(Conversation.user1_id == me,
            Conversation.user2_id == me)
        )
    res = await db.execute(stmt)
    rows = res.scalars().all()

    out: List[str] = []

    for conversation in rows:
        out.append(conversation.user2_id if conversation.user1_id == me else conversation.user1_id)

    return [DomainConversation(with_user=user) for user in out]