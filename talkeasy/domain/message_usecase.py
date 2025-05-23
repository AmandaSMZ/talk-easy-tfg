from httpx import HTTPStatusError
from domain.message_domain import DomainMessage
from infraestructure.services.tagging_api import request_tags
from infraestructure.db.repository import get_chat_messages, save_new_message, get_tags_list
from mappers import msgModel_to_msgSenderSchema
from domain.message_domain import DomainMessage
from infraestructure.websockets.connection_manager import connection_manager
from fastapi.encoders import jsonable_encoder


async def send_message(db, msg_in_schema, user_id):

    domain_msg = DomainMessage(
        from_user_id=user_id,
        to_user_id=msg_in_schema.to_user_id,
        content=msg_in_schema.content
    )

    possible_tags = get_tags_list(db)

    try:
        domain_msg.tags = await request_tags(domain_msg.content, possible_tags)

    except HTTPStatusError as e:
       
        print(f"Error etiquetando mensaje: {e}")
        domain_msg.tags = []


    msg_saved = save_new_message(db, domain_msg)

    await connection_manager.send_personal_message(
        {
            "type": "new_message",
            "message": jsonable_encoder(msgModel_to_msgSenderSchema(msg_saved)),
        },
        msg_saved.to_user_id
    )

    return msgModel_to_msgSenderSchema(msg_saved)


def get_chat_between_users(db, user1, user2, last_id=None):
    
    return get_chat_messages(db, user1, user2, last_id)
