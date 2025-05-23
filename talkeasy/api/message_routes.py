from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from infraestructure.db.utils import get_db
from api.message_schemas import MessageIn, MessageOut, MessageOutSender, TagsIn
from domain.message_usecase import get_chat_between_users, send_message
from mappers import msgModel_to_msgOutSchema
from infraestructure.db.repository import create_tags
from infraestructure.auth.dependencies import get_current_user

router = APIRouter()

@router.post("/send", response_model=MessageOutSender, status_code=status.HTTP_201_CREATED)
async def send_message_route(msg: MessageIn, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return await send_message(db, msg, user['id'])

@router.get(
    "/chat/{with_user}",
    response_model=list[MessageOut],
    summary="Get conversation with another user"
)
def get_chat(
    with_user: str,
    db: Session = Depends(get_db),
    last_id: int = None,
    user = Depends(get_current_user)
):
    messages = get_chat_between_users(db, user['id'], with_user, last_id)
    
    return [msgModel_to_msgOutSchema(msg) for msg in messages]

@router.post("/tags", status_code=status.HTTP_201_CREATED)
def create_tags_route(tags_in: TagsIn, db: Session = Depends(get_db)):
    if not tags_in.tags:
        raise HTTPException(status_code=400, detail="La lista de etiquetas está vacía")
    
    tag_names = [tag.name for tag in tags_in.tags]
    saved_tags = create_tags(db, tag_names)
    return {"created_tags": [tag.name for tag in saved_tags]}