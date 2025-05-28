from fastapi import APIRouter, Request, status, Depends, HTTPException
from app.dependencies import get_current_user
from app.service import get_available_tags, request_tags
from app.api.schemas import MessageIn
from app.proxy import proxy_request
from config import settings

router = APIRouter()

def user_headers(user):
    return {"X-User-Id": user["user_id"]}

@router.post("/messages/send", status_code=status.HTTP_201_CREATED)
async def proxy_send_message(request: Request, user=Depends(get_current_user)):
    body = await request.json()
    headers = user_headers(user)

    # 1) Proxy request para obtener etiquetas de tagging-api
    tags_response = await proxy_request(
        base_url=settings.TAGGING_API_URL,
        method="POST",
        endpoint="tags/available",
        expected_status_code=200,
        body={"text": body.get("content", ""), "labels": []},  # labels vacíos o los que quieras
        headers=headers
    )
    predicted_tags = tags_response.get("predicted_labels", [])

    # 2) Añadir etiquetas al body
    body["tags"] = predicted_tags

    # 3) Proxy request para enviar mensaje etiquetado a talkeasy
    return await proxy_request(
        base_url=settings.TALKEASY_API_URL,
        method="POST",
        endpoint="messages/send",
        expected_status_code=201,
        body=body,
        headers=headers
    )

    
@router.post("/messagesAA/send", status_code=status.HTTP_201_CREATED)
async def proxy_send_message(request: Request, user=Depends(get_current_user)):
    body = await request.json()
    headers = user_headers(user)
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

@router.post("/tags/add", status_code=status.HTTP_201_CREATED)
async def proxy_create_tags(request: Request, user=Depends(get_current_user)):
    body = await request.json()
    headers = user_headers(user)
    return await proxy_request(
        base_url=settings.TALKEASY_API_URL,
        method="POST",
        endpoint="tags/add",
        expected_status_code=201,
        body=body,
        headers=headers
    )

@router.get("/tags/available")
async def proxy_get_available_tags(user=Depends(get_current_user)):
    headers = user_headers(user)
    return await proxy_request(
        base_url=settings.TALKEASY_API_URL,
        method="GET",
        endpoint="tags/available",
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