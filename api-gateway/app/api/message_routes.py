from fastapi import APIRouter
from fastapi import Depends, HTTPException
import httpx
from services.auth_token import get_current_user
from service import TALKEASY_API_URL, get_available_tags, request_tags
from app.api.schemas import MessageIn



router = APIRouter()

@router.post("/messages/send")
async def send_message(data: MessageIn, user=Depends(get_current_user)):
    try:
        available_tags = await get_available_tags()

        predicted_tags = await request_tags(data.content, available_tags)

        # 3. Enviar el mensaje ya etiquetado al microservicio TalkEasy
        payload = {
            "from_user": data.from_user,
            "to_user": data.to_user,
            "content": data.content,
            "tags": predicted_tags
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{TALKEASY_API_URL}/messages/send", json=payload
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))