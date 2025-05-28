from uuid import UUID
from domain.message_domain import DomainMessage
from infraestructure.db.models import MessageModel
from api.message_schemas import Message, MessageSender, MessageReceiver

# MessageIn --> MessageDomain
def schema_to_domain_message(schema: Message, from_user_id: UUID, tags_id: list[UUID] = None) -> DomainMessage:
    return DomainMessage(
        from_user_id=from_user_id,
        to_user_id=schema.to_user_id,
        text=schema.text,
        tags_id=tags_id or []
    )

# MessageDomain --> MessageOut
def domain_to_schema_message_sender(domain_msg: DomainMessage) -> MessageSender:

    return MessageSender(
        id=domain_msg.id,
        to_user_id=domain_msg.to_user_id,
        text=domain_msg.text,
        timestamp=domain_msg.timestamp,
        from_user_tags=domain_msg.from_user_tags
    )
def domain_to_schema_message_receiver(domain_msg: DomainMessage) -> MessageReceiver:

    return MessageReceiver(
        id=domain_msg.id,
        from_user_id=domain_msg.from_user_id,
        text=domain_msg.text,
        timestamp=domain_msg.timestamp,
        to_user_tags=domain_msg.to_user_tags
    )

def domain_to_schema_message(domain_msg: DomainMessage) -> Message:

    return Message(
        id=domain_msg.id,
        to_user_id=domain_msg.to_user_id,
        from_user_id=domain_msg.from_user_id,
        text=domain_msg.text,
        timestamp=domain_msg.timestamp,
        to_user_tags=domain_msg.to_user_tags,
        from_user_tags=domain_msg.from_user_tags
    )


# MessageModel --> DomainMessage
def db_message_to_domain(
    db_msg: MessageModel, 
    to_user_tags: list[UUID],
    from_user_tags: list[UUID]
    ) -> DomainMessage:

    return DomainMessage(
        id=db_msg.id,
        from_user_id=db_msg.from_user_id,
        to_user_id=db_msg.to_user_id,
        text=db_msg.text,
        timestamp=db_msg.timestamp,
        to_user_tags=to_user_tags,
        from_user_tags=from_user_tags,
        is_read=bool(db_msg.is_read)
    )

# DomainMessage --> MessageModel
def domain_message_to_db_model(domain_msg: DomainMessage) -> MessageModel:
    return MessageModel(
        id=domain_msg.id, 
        from_user_id=domain_msg.from_user_id,
        to_user_id=domain_msg.to_user_id,
        text=domain_msg.text,
        is_read=domain_msg.is_read
    )