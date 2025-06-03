import json
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends
from app.dependencies import get_current_user
from app.api.schemas.message_schemas import MessageOut, MessageIn
from app.api.schemas.user_schemas import UserSearch, UsersIdRequest
from app.proxy import proxy_request
from config import settings
from app.api.utils import convert_uuids_to_str, user_headers
from app.websockets.connection_manager import connection_manager
from app.api.cache.users_cache import user_cache

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


    body['to_user_tags'] = result['to_user_tags']
    body['from_user_tags'] = result['from_user_tags']

    body = convert_uuids_to_str(body)

    to_user_tags = body['to_user_tags']
    from_user_tags = body['from_user_tags']


    messages = await proxy_request(
        base_url=settings.TALKEASY_API_URL,
        method="POST",
        endpoint="messages/send",
        expected_status_code=201,
        body=body,
        headers=headers
    )
    

    messages[0]['tags'] = to_user_tags
    messages[1]['tags'] = from_user_tags

    for msg in messages:
        user_obj = await user_cache.get_user(str(msg['with_user_id']), headers)
        msg['with_user'] = user_obj.model_dump()


    with_user_id = msg["with_user_id"]
    del msg['with_user_id']

    try:
        await connection_manager.send_personal_message(msg, UUID(with_user_id))
    except:
        print('error enviando el mensaje por ws /', with_user_id)

    return messages
        

@router.get("/messages/chat/{with_user}", response_model=List[MessageOut])
async def proxy_get_chat(with_user: str, user=Depends(get_current_user)):
    headers = user_headers(user)
    
    messages = await proxy_request(
        base_url=settings.TALKEASY_API_URL,
        method="GET",
        endpoint=f"messages/chat/{with_user}",
        expected_status_code=200,
        headers=headers
    )

    if not isinstance(messages, list):
        raise HTTPException(status_code=502, detail="Respuesta inesperada del backend de mensajes")

    if not messages:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No se han encontrado mensajes")

    user_ids = {str(msg['with_user_id']) for msg in messages}

    body = UsersIdRequest(users_id=list(user_ids)).model_dump()
    users = await proxy_request(
        base_url=settings.AUTH_API_URL,
        method="POST",
        endpoint="auth/search/users",
        expected_status_code=200,
        headers=headers,
        body=body
    )

    user_map = {user['id']: user for user in users}

    user_tags = await proxy_request(
        base_url=settings.TAGGING_API_URL,
        method="GET",
        endpoint="tags/available",
        expected_status_code=200,
        headers=headers
    )
    tag_id_to_name = {str(tag['id']): tag['name'] for tag in user_tags}

    for msg in messages:
        msg['with_user'] = user_map.get(str(msg['with_user_id']))
        msg['tags'] = [
            {
                "id": tag['id'],
                "name": tag_id_to_name.get(str(tag['id']), "")
            }
            for tag in msg.get('tags', [])
        ]

    return messages


@router.get("/conversations", response_model=List[UserSearch])
async def proxy_list_conversations(user=Depends(get_current_user)):
    headers = user_headers(user)
    user_ids = await proxy_request(
        base_url=settings.TALKEASY_API_URL,
        method="GET",
        endpoint="conversations",
        expected_status_code=200,
        headers=headers
    )

    if not user_ids:
        return []
    user_ids_str = [str(uid) for uid in user_ids]
    body = UsersIdRequest(users_id=user_ids_str).model_dump()
    
    users = await proxy_request(
        base_url=settings.AUTH_API_URL,
        method="POST",
        endpoint="auth/search/users",
        expected_status_code=200,
        headers=headers,
        body=body
    )

    return users


@router.get(
    "/messages/by-tag/{tag_id}",
    summary="Obtiene mensajes por etiqueta para el usuario autenticado",
    response_model=List[MessageOut]
)
async def proxy_get_messages_by_tag(tag_id: UUID, user=Depends(get_current_user)):
    headers = user_headers(user)

    messages = await proxy_request(
        base_url=settings.TALKEASY_API_URL,
        method="GET",
        endpoint=f"messages/by-tag/{tag_id}",
        expected_status_code=200,
        headers=headers
    )

    if not isinstance(messages, list):
        raise HTTPException(status_code=502, detail="Respuesta inesperada del backend de mensajes")

    if not messages:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No se han encontrado mensajes")

    user_ids = {str(msg['with_user_id']) for msg in messages}
    body = UsersIdRequest(users_id=list(user_ids)).model_dump()

    users = await proxy_request(
        base_url=settings.AUTH_API_URL,
        method="POST",
        endpoint="auth/search/users",
        expected_status_code=200,
        headers=headers,
        body=body
    )
    user_map = {user['id']: user for user in users}

    user_tags = await proxy_request(
        base_url=settings.TAGGING_API_URL,
        method="GET",
        endpoint="tags/available",
        expected_status_code=200,
        headers=headers
    )
    tag_id_to_name = {str(tag['id']): tag['name'] for tag in user_tags}

    for msg in messages:
        msg['with_user'] = user_map.get(str(msg['with_user_id']))
        msg['tags'] = [
            {
                "id": tag['id'],
                "name": tag_id_to_name.get(str(tag['id']), "")
            }
            for tag in msg.get('tags', [])
        ]

    return messages
