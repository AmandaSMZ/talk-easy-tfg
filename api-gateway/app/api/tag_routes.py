from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.dependencies import get_current_user
from app.proxy import proxy_request
from config import settings
from app.api.schemas import TagIn
from app.api.utils import user_headers

router = APIRouter()


@router.post("/tags/add", status_code=status.HTTP_201_CREATED)
async def proxy_send_message(request: List[TagIn], user=Depends(get_current_user)):
    body =  [tag.model_dump() for tag in request]
    headers = user_headers(user)

    return await proxy_request(
        base_url=settings.TAGGING_API_URL,
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
        base_url=settings.TAGGING_API_URL,
        method="GET",
        endpoint="tags/available",
        expected_status_code=200,
        headers=headers
    )

@router.delete("/tags/delete/{tag_id}")
async def proxy_delete_tag(tag_id: UUID, user=Depends(get_current_user)):
    headers = user_headers(user)
    return await proxy_request(
        base_url=settings.TAGGING_API_URL,
        method="DELETE",
        endpoint=f"tags/delete/{tag_id}",
        expected_status_code=200,
        headers=headers
    )