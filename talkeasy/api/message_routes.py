from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from infraestructure.db.utils import get_db
from api.message_schemas import MessageIn, MessageOutSender
from domain.message_usecase import send_message

router = APIRouter()

@router.post("/send", response_model=MessageOutSender, status_code=status.HTTP_201_CREATED)
async def send_message_route(msg: MessageIn, db: Session = Depends(get_db)):

    return await send_message(db, msg)