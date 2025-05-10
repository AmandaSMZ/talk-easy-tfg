from sqlalchemy.orm import Session
from models import Message, MessageTag

def save_message(db: Session, domain_msg) -> tuple:
    # Guardar mensaje base
    db_msg = Message(
        from_user=domain_msg.from_user,
        to_user=domain_msg.to_user,
        content=domain_msg.content,
        timestamp=domain_msg.timestamp,
        is_read=1 if domain_msg.is_read else 0
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)

    # Guardar tags
    tag_objs = []
    for tag in domain_msg.tags:
        db_tag = MessageTag(message_id=db_msg.id, tag=tag)
        db.add(db_tag)
        tag_objs.append(db_tag)
    db.commit()

    return db_msg, tag_objs