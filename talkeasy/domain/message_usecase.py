from typing import List
from uuid import UUID
from domain.message_domain import DomainMessage, DomainTag
from infraestructure.db.repository import create_conversation_if_not_exists, create_tags, get_chat_messages, get_tag_ids_by_names, get_tags_list, list_interlocutors, save_new_message
from mappers import domain_tag_to_schema_tag, domain_to_schema_message
from domain.message_domain import DomainMessage
from infraestructure.websockets.connection_manager import connection_manager
from fastapi.encoders import jsonable_encoder
from api.message_schemas import Conversation, MessageIn, Tag
from sqlalchemy.ext.asyncio import AsyncSession

async def send_message(db: AsyncSession, schema: MessageIn, from_user_id: UUID):

    tag_ids = await get_tag_ids_by_names(db, schema.tags or [])
    domain_msg = DomainMessage(
        from_user_id=from_user_id,
        to_user_id=schema.to_user_id,
        content=schema.content,
        tags=tag_ids
    )

    msg_saved = await save_new_message(db, domain_msg)
    
    await create_conversation_if_not_exists(db, msg_saved.from_user_id, msg_saved.to_user_id)

    msg_out = domain_to_schema_message(msg_saved)

    await connection_manager.send_personal_message(
        {
            "type": "new_message",
            "message": jsonable_encoder(msg_out),
        },
        msg_saved.to_user_id
    )

    return msg_out


async def get_chat_between_users(db: AsyncSession, user1, user2, last_id=None):
    result = await get_chat_messages(db, user1, user2, last_id)
    return [domain_to_schema_message(message) for message in result]

async def create_tags_use_case(db: AsyncSession, tags:List[str]):

    tags_domain = [DomainTag(name=tag.name) for tag in tags]
    created_tags = await create_tags(db,tags_domain)
    return [Tag(name=tag.name, id=tag.id) for tag in created_tags]

async def get_tags(db:AsyncSession):
    tags = await get_tags_list(db)
    return [domain_tag_to_schema_tag(tag) for tag in tags]

async def list_conversations_use_case(
    db: AsyncSession,
    me: UUID
) -> List[Conversation]:
    result = await list_interlocutors(db, me)
    print('RESULTADO: ', result)
    return [Conversation(id = user_id) for user_id in result]