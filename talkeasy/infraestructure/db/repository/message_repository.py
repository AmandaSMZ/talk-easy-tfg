from typing import List, Optional
from uuid import UUID
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.message_domain import DomainMessage, DomainTag
from infraestructure.db.repository.base import IMessageRepository
from infraestructure.db.models import Conversation, MessageModel, MessageTagUserModel
from mappers import db_message_to_domain, domain_message_to_db_model

class SQLAlchemyMessageRepository(IMessageRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_message(self, message: DomainMessage) -> DomainMessage:
        db_msg = domain_message_to_db_model(message)
        self.db.add(db_msg)
        await self.db.commit()
        await self.db.refresh(db_msg)

        to_user_tags_id = [tag.id for tag in message.to_user_tags] if message.to_user_tags else []
        if to_user_tags_id:
            await self._update_message_tags(db_msg.to_user_id, db_msg.id, to_user_tags_id)

        from_user_tags_id = [tag.id for tag in message.from_user_tags] if message.from_user_tags else []
        if from_user_tags_id:
            await self._update_message_tags(db_msg.from_user_id, db_msg.id, from_user_tags_id)

        message.id = db_msg.id
        message.timestamp = db_msg.timestamp

        return message
    
    async def _update_message_tags(self, user_id: UUID, msg_id: UUID, tags: List[UUID]):
        tag_objs = [
            MessageTagUserModel(message_id=msg_id, user_id=user_id, tag_id=tag_id)
            for tag_id in tags
        ]
        self.db.add_all(tag_objs)
        await self.db.commit()

    async def get_messages_by_chat(self, user1: UUID, user2: UUID, last_id: Optional[UUID] = None) -> List[DomainMessage]:
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
        res = await self.db.execute(stmt)
        messages = res.scalars().all()

        result = []
        for msg in messages:
            result_from = await self.db.execute(
                select(MessageTagUserModel.tag_id).where(
                    MessageTagUserModel.message_id == msg.id,
                    MessageTagUserModel.user_id == msg.from_user_id
                )
            )
            from_user_tag_ids = result_from.scalars().all()
            from_user_tags = [DomainTag(id=tag_id, name="") for tag_id in from_user_tag_ids]

            result_to = await self.db.execute(
                select(MessageTagUserModel.tag_id).where(
                    MessageTagUserModel.message_id == msg.id,
                    MessageTagUserModel.user_id == msg.to_user_id
                )
            )
            to_user_tag_ids = result_to.scalars().all()
            to_user_tags = [DomainTag(id=tag_id, name="") for tag_id in to_user_tag_ids]

            domain_msg = DomainMessage(
                id=msg.id,
                from_user_id=msg.from_user_id,
                to_user_id=msg.to_user_id,
                text=msg.text,
                timestamp=msg.timestamp,
                from_user_tags=from_user_tags,
                to_user_tags=to_user_tags,
                is_read=msg.is_read or False
            )
            result.append(domain_msg)

        return result

    async def get_messages_by_tag(self, user_id: UUID, tag_id: UUID) -> List[DomainMessage]:
        
        result = await self.db.execute(
            select(MessageTagUserModel.message_id)
            .where(
            and_(
                MessageTagUserModel.tag_id == tag_id,
                MessageTagUserModel.user_id == user_id
            )
             )
        )


        message_ids = [row[0] for row in result.all()]

        print(message_ids)

        if not message_ids:
            return []

        result = await self.db.execute(
        select(MessageModel)
            .where(
            and_(
                MessageModel.id.in_(message_ids),
            or_(
                MessageModel.from_user_id == user_id,
                MessageModel.to_user_id == user_id
            )
        )
        )
        .order_by(MessageModel.timestamp.desc())
        )
        messages = result.scalars().all()
        print('------------------------')
        print(len(messages))
        domain_messages = []

        for msg in messages:
            domain_msg = db_message_to_domain(msg)
            domain_messages.append(domain_msg)

        return domain_messages

    async def list_conversations(self, user_id: UUID) -> List[UUID]:
        stmt = select(Conversation).where(
            or_(
                Conversation.user1_id == user_id,
                Conversation.user2_id == user_id
            )
        )
        res = await self.db.execute(stmt)
        rows = res.scalars().all()

        interlocutors = []
        for conv in rows:
            interlocutors.append(conv.user2_id if conv.user1_id == UUID(str(user_id)) else conv.user1_id)

        return list(set(interlocutors))

    async def create_conversation_if_not_exists(self, user1: UUID, user2: UUID) -> None:
        u1, u2 = sorted([user1, user2], key=str)
        query = select(Conversation).where(
            (Conversation.user1_id == u1) & (Conversation.user2_id == u2)
        )
        result = await self.db.execute(query)
        conv = result.scalar_one_or_none()

        if not conv:
            conv = Conversation(user1_id=u1, user2_id=u2)
            self.db.add(conv)
            await self.db.commit()
