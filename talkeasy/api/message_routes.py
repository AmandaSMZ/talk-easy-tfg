from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from infraestructure.db.utils import get_db
from api.message_schemas import Conversation, MessageIn, MessageOut, Tag, TagIn
from domain.message_usecase import create_tags_use_case, get_chat_between_users, get_tags, list_conversations_use_case, send_message
from infraestructure.auth.dependencies import get_current_user, verify_internal_token_only

router = APIRouter(dependencies=[Depends(verify_internal_token_only)])

@router.post(
        "/send", 
        response_model=MessageOut, 
        status_code=status.HTTP_201_CREATED)
async def send_message_route(
    msg: MessageIn, 
    db: AsyncSession = Depends(get_db), 
    user = Depends(get_current_user)
):
    return await send_message(db, msg, user['id'])

@router.get(
    "/chat/{with_user}",
    response_model=list[MessageOut],
    summary="Get conversation with another user"
)
async def get_chat(
    with_user: UUID,
    db: AsyncSession = Depends(get_db),
    last_id: UUID = None,
    user = Depends(get_current_user)
):
    return await get_chat_between_users(db, user['id'], with_user, last_id)


@router.post("/tags/add", status_code=status.HTTP_201_CREATED)
async def create_tags_route(
    tags_in: List[TagIn],
    db: AsyncSession = Depends(get_db)
):
    if not tags_in:
        raise HTTPException(status_code=400, detail="La lista de etiquetas está vacía")
    
    return await create_tags_use_case(db, tags_in)


@router.get("/tags/available", response_model=list[Tag])
async def get_available_tags_route(db: AsyncSession = Depends(get_db)):
    return await get_tags(db)


@router.get(
    "/conversations",
    response_model=List[Conversation],
    summary="Lista de IDs de usuarios con los que has conversado"
)
async def list_conversations_route(
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user),
):
    return await list_conversations_use_case(db, user["id"])