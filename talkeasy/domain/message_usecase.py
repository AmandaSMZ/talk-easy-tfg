from typing import List
from uuid import UUID

from fastapi import HTTPException
from infraestructure.db.repository.base import IMessageRepository
from mappers import domain_to_schema_message, map_domain_to_message_out, schema_to_domain_message
from infraestructure.websockets.connection_manager import connection_manager
from api.message_schemas import MessageIn, MessageOut, Tag

async def send_message(repo: IMessageRepository, msg_in: MessageIn, from_user_id: UUID):
    try:
        domain_msg = schema_to_domain_message(msg_in, from_user_id)
        msg_saved = await repo.save_message(domain_msg)
        await repo.create_conversation_if_not_exists(msg_saved.from_user_id, msg_saved.to_user_id)

        msg_out_receiver = domain_to_schema_message(msg_saved, current_user_id=msg_saved.to_user_id)
        msg_out_receiver.tags = msg_in.to_user_tags or []

        await connection_manager.send_personal_message(
            {
                "type": "new_message",
                "message": msg_out_receiver.model_dump(),
            },
            msg_saved.to_user_id
        )

        msg_out_sender = domain_to_schema_message(msg_saved, current_user_id=from_user_id)
        msg_out_sender.tags = msg_in.from_user_tags or []
        return msg_out_sender

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar mensaje: {str(e)}")


async def get_chat_between_users(repo: IMessageRepository, current_user:UUID, with_user_id:UUID, last_id:UUID=None):
    messages = await repo.get_messages_by_chat(current_user, with_user_id, last_id)
    response = []

    for msg in messages:
        msg_type = "received" if msg.to_user_id == current_user else "sent"

        user_tags = msg.from_user_tags if msg_type == "sent" else msg.to_user_tags

        msg_out = MessageOut(
            id=msg.id,
            text=msg.text,
            timestamp=msg.timestamp,
            type=msg_type,
            tags=[Tag(id=tag.id, name="") for tag in user_tags],
        )
        response.append(msg_out)

    return response


async def list_conversations_use_case(
    repo: IMessageRepository,
    user_id: UUID
) -> List[UUID]:
    result = await repo.list_conversations(user_id)
    return result

async def get_messages_by_tag_use_case(repo: IMessageRepository, user_id:UUID, tag_id:UUID) -> List[MessageOut]:
    domain_messages = await repo.get_messages_by_tag(tag_id=tag_id, user_id=user_id)
    print('----------------------------------------------------------------------------------------')
    print (len(domain_messages))
    print('-----------------------------------------------------------------------------------')
    return map_domain_to_message_out(domain_messages, user_id)