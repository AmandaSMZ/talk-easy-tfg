from sqlalchemy.orm import Session
from infraestructure.postgres.models.message_model import Message

def save_message(db: Session, sender: str, recipient: str, content: str, label: str):
    message = Message(
        sender=sender,
        recipient=recipient,
        content=content,
        label=label
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message