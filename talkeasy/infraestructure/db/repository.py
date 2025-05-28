from typing import List, Optional
from uuid import UUID
from sqlalchemy import and_, or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.message_domain import DomainConversation
from infraestructure.db.models import Conversation, MessageModel, MessageTagUserModel
from mappers import db_message_to_domain, domain_message_to_db_model

async def save_new_message(db: AsyncSession, domain_msg):

    db_msg = domain_message_to_db_model(domain_msg)

    db.add(db_msg)
    await db.commit()
    await db.refresh(db_msg)

    to_user_tags_id = domain_msg.to_user_tags or []
    if to_user_tags_id:
        await update_message_tags(db, db_msg.to_user_id, db_msg.id, to_user_tags_id)

    from_user_tags_id = domain_msg.from_user_tags or []
    if from_user_tags_id:
        await update_message_tags(db,db_msg.from_user_id, db_msg.id, from_user_tags_id)

    return db_message_to_domain(db_msg=db_msg,to_user_tags=to_user_tags_id,from_user_tags=from_user_tags_id)
    

async def update_message_tags(db: AsyncSession,user_id:UUID, msg_id:UUID, tags: list[UUID]):

    tag_objs = [
        MessageTagUserModel(message_id=msg_id,
                            user_id=user_id,
                            tag_id=tag_id) 
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
        result_from = await db.execute(
            select(MessageTagUserModel.tag_id).where(
                MessageTagUserModel.message_id == msg.id,
                MessageTagUserModel.user_id == msg.from_user_id
            )
        )
        from_user_tag_ids = result_from.scalars().all()

        result_to = await db.execute(
            select(MessageTagUserModel.tag_id).where(
                MessageTagUserModel.message_id == msg.id,
                MessageTagUserModel.user_id == msg.to_user_id
            )
        )
        to_user_tag_ids = result_to.scalars().all()
        

        domain_msg = db_message_to_domain(msg, to_user_tags=to_user_tag_ids, from_user_tags=from_user_tag_ids)
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