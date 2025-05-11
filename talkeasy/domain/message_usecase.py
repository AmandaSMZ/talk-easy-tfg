from domain.message_domain import DomainMessage
from infraestructure.services.tagging_api import request_tags
from infraestructure.db.repository import save_new_message, get_tags_list
from mappers import msgModel_to_msgSenderSchema

async def send_message(db, msg_in_schema):
    domain_msg = DomainMessage(
        from_user=msg_in_schema.from_user,
        to_user=msg_in_schema.to_user,
        content=msg_in_schema.content
    )

    possible_tags = get_tags_list(db)

    domain_msg.tags = await request_tags(domain_msg.content, possible_tags)

    msg = save_new_message(db, domain_msg)

    return msgModel_to_msgSenderSchema(msg)