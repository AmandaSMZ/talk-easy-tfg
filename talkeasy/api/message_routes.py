from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from message_schemas import MessageIn, MessageOut
from domain.message_usecase import send_message
from infraestructure.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/send", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def send_message_route(msg: MessageIn, db: Session = Depends(get_db)):
    # 1. Flujo principal con arquitectura limpia
    domain_msg, db_msg, tag_objs = await send_message(db, msg)
    # 2. Devuelve el schema OUT (puedes montar manualmente o con Pydantic)
    return MessageOut(
        from_user=domain_msg.from_user,
        to_user=domain_msg.to_user,
        content=domain_msg.content,
        timestamp=domain_msg.timestamp,
        tags=domain_msg.tags,
        is_read=domain_msg.is_read
    )