from uuid import UUID
from domain.message_domain import DomainMessage, DomainTag
from infraestructure.db.models import MessageModel
from api.message_schemas import MessageIn, MessageOut, Tag

# MessageIn --> MessageDomain
def schema_to_domain_message(schema: MessageIn, from_user_id: UUID, tags_id: list[UUID] = None) -> DomainMessage:
    return DomainMessage(
        from_user_id=from_user_id,
        to_user_id=schema.to_user_id,
        content=schema.content,
        tags_id=tags_id or []
    )

# MessageDomain --> MessageOut
def domain_to_schema_message(domain_msg: DomainMessage) -> MessageOut:
    tags = None
    if domain_msg.tags:
        tags = [Tag(id=tag.id, name=tag.name) for tag in domain_msg.tags]

    return MessageOut(
        id=domain_msg.id,
        to_user_id=domain_msg.to_user_id,
        content=domain_msg.content,
        timestamp=domain_msg.timestamp,
        tags=tags
    )


# MessageModel --> DomainMessage
def db_message_to_domain(
    db_msg: MessageModel, 
    db_tags: list[TagsModel]
    ) -> DomainMessage:

    domain_tags = [DomainTag(id=tag.id, name=tag.name) for tag in db_tags]

    return DomainMessage(
        id=db_msg.id,
        from_user_id=db_msg.from_user_id,
        to_user_id=db_msg.to_user_id,
        content=db_msg.content,
        timestamp=db_msg.timestamp,
        tags=domain_tags,
        is_read=bool(db_msg.is_read)
    )

# DomainMessage --> MessageModel
def domain_message_to_db_model(domain_msg: DomainMessage) -> MessageModel:
    return MessageModel(
        id=domain_msg.id, 
        from_user_id=domain_msg.from_user_id,
        to_user_id=domain_msg.to_user_id,
        content=domain_msg.content,
        is_read=domain_msg.is_read
    )