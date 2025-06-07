from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status
from api.message_schemas import MessageOut, MessageIn
from domain.message_usecase import (get_chat_between_users,
                                    get_messages_by_tag_use_case,
                                    list_conversations_use_case,
                                    send_message)
from dependencies import get_current_user
from infraestructure.db.repository.base import IMessageRepository
from infraestructure.db.dependencies.repository import get_message_repository

router = APIRouter()


@router.post(
        "/messages/send",
        response_model=List[MessageOut],
        status_code=status.HTTP_201_CREATED,
        summary="Envía un mensaje a un usuario"
        )
async def send_message_route(
    msg: MessageIn,
    repo: IMessageRepository = Depends(get_message_repository),
    user_id=Depends(get_current_user)
):
    return await send_message(repo=repo, msg_in=msg, from_user_id=user_id)


@router.get(
    "/messages/chat/{with_user}",
    response_model=List[MessageOut],
    summary="Obtiene los mensajes con un usuario específico"
)
async def get_chat(
    with_user: UUID,
    repo: IMessageRepository = Depends(get_message_repository),
    last_id: Optional[UUID] = None,
    user_id=Depends(get_current_user)
):
    return await get_chat_between_users(repo,
                                        current_user=user_id,
                                        with_user_id=with_user,
                                        last_id=last_id)


@router.get(
    "/conversations",
    response_model=List[UUID],
    summary="Lista de IDs de usuarios con los que ha conversado el usuario"
)
async def list_conversations_route(
    repo: IMessageRepository = Depends(get_message_repository),
    user_id=Depends(get_current_user)
):
    return await list_conversations_use_case(repo, user_id)


@router.get(
    "/messages/by-tag/{tag_id}",
    response_model=List[MessageOut],
    summary="Devuelve todos los mensajes del usuario (enviados y recibidos) \
          con una etiqueta específica"
)
async def get_messages_by_tag(
    tag_id: UUID,
    repo: IMessageRepository = Depends(get_message_repository),
    user_id=Depends(get_current_user)
):
    return await get_messages_by_tag_use_case(repo,
                                              user_id=user_id,
                                              tag_id=tag_id)
