from typing import List
from uuid import UUID
from domain.message_domain import DomainMessage
from infraestructure.db.repository import create_conversation_if_not_exists, get_chat_messages, get_messages_by_tag, list_interlocutors, save_new_message
from mappers import domain_to_schema_message, domain_to_schema_message_receiver, domain_to_schema_message_sender
from domain.message_domain import DomainMessage
from infraestructure.websockets.connection_manager import connection_manager
from fastapi.encoders import jsonable_encoder
from api.message_schemas import Conversation, Message
from sqlalchemy.ext.asyncio import AsyncSession

async def send_message(db: AsyncSession, schema: Message, from_user_id: UUID):

    domain_msg = DomainMessage(
        from_user_id=from_user_id,
        to_user_id=schema.to_user_id,
        text=schema.text,
        from_user_tags=schema.from_user_tags,
        to_user_tags=schema.to_user_tags
    )

    msg_saved = await save_new_message(db, domain_msg)
    
    await create_conversation_if_not_exists(db, msg_saved.from_user_id, msg_saved.to_user_id)

    msg_out_receiver = domain_to_schema_message_receiver(msg_saved)

    await connection_manager.send_personal_message(
        {
            "type": "new_message",
            "message": jsonable_encoder(msg_out_receiver),
        },
        msg_saved.to_user_id
    )

    return domain_to_schema_message_sender(msg_saved)


async def get_chat_between_users(db: AsyncSession, user1, user2, last_id=None):
    result = await get_chat_messages(db, user1, user2, last_id)
    return [domain_to_schema_message(message) for message in result]


async def list_conversations_use_case(
    db: AsyncSession,
    me: UUID
) -> List[Conversation]:
    result = await list_interlocutors(db, me)
    print('RESULTADO: ', result)
    return [Conversation(user_id = conv.with_user) for conv in result]

async def get_messages_by_tag_use_case(db, user_id, tag_id) -> List[Message]:
    domain_messages = await get_messages_by_tag(db, tag_id, user_id)
    return [domain_to_schema_message(msg) for msg in domain_messages]