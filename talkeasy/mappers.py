from domain.message_domain import DomainMessage
from infraestructure.db.models import MessageModel, TagsModel
from typing import List
from api.message_schemas import MessageOut, MessageOutSender

def db_models_to_domain(db_msg: MessageModel, tags: List[str]) -> DomainMessage:
    return DomainMessage(
        id=db_msg.id,
        from_user=db_msg.from_user,
        to_user=db_msg.to_user,
        content=db_msg.content,
        timestamp=db_msg.timestamp,
        tags=tags,
        is_read=bool(db_msg.is_read)
    )

def msgModel_to_msgSenderSchema(msgDomain: DomainMessage):
    return MessageOutSender(
        content=msgDomain.content,
        timestamp=msgDomain.timestamp,
        tags=msgDomain.tags
    )

def msgModel_to_msgOutSchema(msgDomain: DomainMessage):
    return MessageOut(
        id=msgDomain.id,
        from_user=msgDomain.from_user,
        to_user=msgDomain.to_user,
        content=msgDomain.content,
        timestamp=msgDomain.timestamp,
        tags=msgDomain.tags,
        )