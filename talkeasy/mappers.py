from typing import List, Optional
from uuid import UUID
from domain.message_domain import DomainMessage, DomainTag
from infraestructure.db.models import MessageModel
from api.message_schemas import MessageIn, MessageOut, Tag

def tags_schema_to_domain(tags: Optional[List[Tag]]) -> List[DomainTag]:
    if not tags:
        return []
    return [DomainTag(id=UUID(tag.id), name=tag.name) for tag in tags]

def tags_domain_to_schema(tags: List[DomainTag]) -> List[Tag]:
    return [Tag(id=str(tag.id), name=tag.name) for tag in tags]

def schema_to_domain_message(msg_in: MessageIn, from_user_id: str) -> DomainMessage:
    return DomainMessage(
        id=None,
        from_user_id=UUID(from_user_id),
        to_user_id=UUID(msg_in.to_user_id),
        text=msg_in.text,
        timestamp=None,
        from_user_tags=tags_schema_to_domain(msg_in.from_user_tags),
        to_user_tags=tags_schema_to_domain(msg_in.to_user_tags),
        is_read=False,
    )

def domain_to_schema_message(domain_msg: DomainMessage, current_user_id: UUID) -> MessageOut:

    msg_type = "sent" if domain_msg.from_user_id == current_user_id else "received"
    with_user = domain_msg.from_user_id if msg_type == 'sent' else domain_msg.to_user_id
    tags = domain_msg.from_user_tags if msg_type == "sent" else domain_msg.to_user_tags

    return MessageOut(
        id=str(domain_msg.id),
        with_user_id= str(with_user),
        text=domain_msg.text,
        timestamp=domain_msg.timestamp,
        type=msg_type,
        tags=tags_domain_to_schema(tags),
    )

def domain_message_to_db_model(domain_msg) -> MessageModel:
    return MessageModel(
        id=domain_msg.id or None,
        from_user_id=domain_msg.from_user_id,
        to_user_id=domain_msg.to_user_id,
        text=domain_msg.text,
        timestamp=domain_msg.timestamp,
        is_read=domain_msg.is_read
    )

def db_message_to_domain(
    msg: MessageModel,
    from_user_tags: list[UUID] = None,
    to_user_tags: list[UUID] = None
) -> DomainMessage:
    return DomainMessage(
        id=msg.id,
        from_user_id=msg.from_user_id,
        to_user_id=msg.to_user_id,
        text=msg.text,
        timestamp=msg.timestamp,
        is_read=msg.is_read if msg.is_read is not None else False,
        from_user_tags=[DomainTag(id=tag_id, name="") for tag_id in (from_user_tags or [])],
        to_user_tags=[DomainTag(id=tag_id, name="") for tag_id in (to_user_tags or [])]
    )

def map_domain_to_message_out(messages: List[DomainMessage], user_id: UUID) -> List[MessageOut]:
    message_out_list: List[MessageOut] = []

    for msg in messages:
        if str(msg.to_user_id) == str(user_id):
            message_type = "received"
            tags = [Tag(id=str(tag.id), name='') for tag in msg.to_user_tags]
            with_user_id = str(msg.from_user_id)
        else:
            message_type = "sent"
            tags = [Tag(id=str(tag.id), name='') for tag in msg.from_user_tags]
            with_user_id = msg.to_user_id

        message_out = MessageOut(
            id=str(msg.id),
            text=msg.text,
            with_user_id=str(with_user_id),
            timestamp=msg.timestamp,
            type=message_type,
            tags=tags
        )
        message_out_list.append(message_out)

    return message_out_list