from domain.message_domain import DomainMessage
from infraestructure.db.models import MessageModel, TagsModel
from typing import List

def db_models_to_domain(db_msg: MessageModel, tag_objs: List[TagsModel]) -> DomainMessage:
    return DomainMessage(
        id=db_msg.id,
        from_user=db_msg.from_user,
        to_user=db_msg.to_user,
        content=db_msg.content,
        timestamp=db_msg.timestamp,
        tags=[t.name for t in tag_objs],
        is_read=bool(db_msg.is_read)
    )