from fastapi import APIRouter, Request
from fastapi import Depends, HTTPException
import httpx
from dependencies import get_current_user
from service import TALKEASY_API_URL, get_available_tags, request_tags
from app.api.schemas import MessageIn
from proxy import proxy_request


router = APIRouter(dependencies=Depends(get_current_user))

@router.post("/messages/send")
async def send_message(data: MessageIn, user=Depends(get_current_user), request: Request = None):
    try:

        available_tags = await get_available_tags()

        predicted_tags = await request_tags(data.content, available_tags)

        payload = {
            "to_user": data.to_user,
            "content": data.content,
            "tags": predicted_tags
        }

        return await proxy_request(request, TALKEASY_API_URL, user, json_data=payload)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))