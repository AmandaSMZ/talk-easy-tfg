from collections import defaultdict
from typing import List, Optional
from uuid import UUID
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.message_domain import DomainMessage, DomainTag
from infraestructure.db.repository.base import IMessageRepository
from infraestructure.db.models import (Conversation,
                                       MessageModel,
                                       MessageTagUserModel)
from mappers import db_message_to_domain, domain_message_to_db_model


class SQLAlchemyMessageRepository(IMessageRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_message(self, message: DomainMessage):
        db_msg = domain_message_to_db_model(message)
        self.db.add(db_msg)

        await self.db.flush()
        await self.db.refresh(db_msg)

        await self._add_message_tags(db_msg, message)

        await self._ensure_conversation(db_msg.from_user_id, db_msg.to_user_id)
        await self.db.commit()

        message.id = db_msg.id
        message.timestamp = db_msg.timestamp

        return message

    async def _add_message_tags(
            self,
            db_msg: MessageModel,
            message: DomainMessage) -> None:
        """Añade todos los tag-objects a la sesión, sin hacer commit."""
        tag_objs: List[MessageTagUserModel] = []

        for tag in message.to_user_tags or []:
            tag_objs.append(
                MessageTagUserModel(
                    message_id=db_msg.id,
                    user_id=db_msg.to_user_id,
                    tag_id=tag.id
                )
            )

        for tag in message.from_user_tags or []:
            tag_objs.append(
                MessageTagUserModel(
                    message_id=db_msg.id,
                    user_id=db_msg.from_user_id,
                    tag_id=tag.id
                )

            )

        if tag_objs:
            self.db.add_all(tag_objs)
            await self.db.flush()

    async def _ensure_conversation(self, u_from: UUID, u_to: UUID) -> None:
        """Busca/crea la conversación en la misma transacción."""

        u1, u2 = sorted([u_from, u_to], key=lambda u: str(u))
        stmt = select(Conversation).where(
            and_(
                Conversation.user1_id == u1,
                Conversation.user2_id == u2
            )
        )
        res = await self.db.execute(stmt)
        conv = res.scalar_one_or_none()
        if conv is None:
            self.db.add(Conversation(user1_id=u1, user2_id=u2))
            await self.db.flush()

    async def get_messages_by_chat(
            self, current_user: UUID,
            with_user: UUID,
            last_id: Optional[UUID] = None) -> List[DomainMessage]:
        # Query para obtener los mensajes del chat
        stmt = select(MessageModel).where(
            or_(
                and_(MessageModel.from_user_id == current_user,
                     MessageModel.to_user_id == with_user),
                and_(MessageModel.from_user_id == with_user,
                     MessageModel.to_user_id == current_user)
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

        message_ids = [msg.id for msg in messages]
        if not message_ids:
            return []

        tag_stmt = select(
            MessageTagUserModel.message_id,
            MessageTagUserModel.user_id,
            MessageTagUserModel.tag_id
        ).where(
            MessageTagUserModel.message_id.in_(message_ids)
        )
        tag_res = await self.db.execute(tag_stmt)
        tags_data = tag_res.all()

        tags_map = defaultdict(list)
        for message_id, user_id, tag_id in tags_data:
            tags_map[(message_id, user_id)].append(
                DomainTag(id=tag_id, name=""))

        result = []
        for msg in messages:
            from_user_tags = tags_map.get((msg.id, msg.from_user_id), [])
            to_user_tags = tags_map.get((msg.id, msg.to_user_id), [])

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

    async def get_messages_by_tag(
            self,
            user_id: UUID,
            tag_id: UUID) -> List[DomainMessage]:
        stmt = select(MessageModel).join(
            MessageTagUserModel,
            MessageModel.id == MessageTagUserModel.message_id).where(
            and_(
                MessageTagUserModel.user_id == user_id,
                MessageTagUserModel.tag_id == tag_id,
                or_(
                    MessageModel.from_user_id == user_id,
                    MessageModel.to_user_id == user_id
                )
                )
            ).order_by(MessageModel.timestamp.asc())

        result = await self.db.execute(stmt)
        messages = result.scalars().all()
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
            interlocutors.append(
                conv.user2_id if conv.user1_id == UUID(str(user_id))
                else conv.user1_id)

        return list(set(interlocutors))
