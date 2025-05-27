import logging
from fastapi import APIRouter, Depends
from app.api.schemas import TagRequest, TagResponse
from app.infraestructure.service import classifier_service
from app.infraestructure.db.db import get_db
from app.domain.use_cases import get_tags
from app.infraestructure.dependencies import get_current_user

logger = logging.getLogger("uvicorn.error")

router = APIRouter()

@router.post("/tag-message", response_model=TagResponse)
async def tag_message(request: TagRequest, 
                db=Depends(get_db),
                user_id=Depends(get_current_user)):
    from_user_tags = await get_tags(db, user_id)
    to_user_tags = await get_tags(db, request.to_user)

    from_user_response = classifier_service.tag_message(request.text, from_user_tags)
    to_user_response = classifier_service.tag_message(request.text, to_user_tags)

    logger.info(f"Petición:{request}, Respuesta: {from_user_response}&{to_user_response}")

    return TagResponse(to_user_tags=to_user_response, from_user_tags=from_user_response)