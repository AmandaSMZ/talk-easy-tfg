import json
from typing import List
from uuid import UUID
from fastapi import APIRouter, status, Depends
from app.dependencies import get_current_user
from app.api.schemas import MessageIn
from app.proxy import proxy_request
from config import settings
from app.api.utils import user_headers

router = APIRouter()


@router.post("/messages/send", status_code=status.HTTP_201_CREATED)
async def proxy_send_message(request: MessageIn, user=Depends(get_current_user)):
    body = request.model_dump()
    headers = user_headers(user)

    result = await proxy_request(
        base_url=settings.TAGGING_API_URL,
        method="POST",
        endpoint="tag-message",
        expected_status_code=200,
        body=body,
        headers=headers
    )
    result = json.loads(result.body)


    body['to_user_tags'] = result['to_user_tags']
    body['from_user_tags'] = result['from_user_tags']


    return await proxy_request(
        base_url=settings.TALKEASY_API_URL,
        method="POST",
        endpoint="messages/send",
        expected_status_code=201,
        body=body,
        headers=headers
    )



@router.get("/messages/chat/{with_user}")
async def proxy_get_chat(with_user: str, user=Depends(get_current_user)):
    headers = user_headers(user)
    endpoint = f"messages/chat/{with_user}"
    return await proxy_request(
        base_url=settings.TALKEASY_API_URL,
        method="GET",
        endpoint=endpoint,
        expected_status_code=200,
        headers=headers
    )


@router.get("/conversations")
async def proxy_list_conversations(user=Depends(get_current_user)):
    headers = user_headers(user)
    return await proxy_request(
        base_url=settings.TALKEASY_API_URL,
        method="GET",
        endpoint="conversations",
        expected_status_code=200,
        headers=headers
    )

@router.get(
    "/messages/by-tag/{tag_id}",
    summary="Obtiene mensajes por etiqueta para el usuario autenticado"
)
async def proxy_get_messages_by_tag(tag_id: UUID, user=Depends(get_current_user)):
    headers = user_headers(user)
    return await proxy_request(
        base_url=settings.TALKEASY_API_URL,
        method="GET",
        endpoint=f"messages/by-tag/{tag_id}",
        expected_status_code=200,
        headers=headers
    )