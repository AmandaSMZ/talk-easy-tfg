from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from infraestructure.db.utils import get_db
from api.message_schemas import MessageIn, MessageOut, MessageOutSender
from domain.message_usecase import get_chat_between_users, send_message
from mappers import msgModel_to_msgOutSchema

router = APIRouter()

@router.post("/send", response_model=MessageOutSender, status_code=status.HTTP_201_CREATED)
async def send_message_route(msg: MessageIn, db: Session = Depends(get_db)):

    return await send_message(db, msg)

@router.get(
    "/chat/{with_user}",
    response_model=list[MessageOut],
    summary="Get conversation with another user"
)
def get_chat(
    with_user: str,
    db: Session = Depends(get_db),
    current_user: str = None,
    last_id: int = None
):
    if current_user is None:
        raise HTTPException(status_code=400, detail="current_user must be provided as query param")
    messages = get_chat_between_users(db, current_user, with_user, last_id)
    
    return [msgModel_to_msgOutSchema(msg) for msg in messages]