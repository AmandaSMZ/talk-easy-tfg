import logging
from typing import List
from fastapi import APIRouter, Depends
from app.api.schemas import TagRequest, TagResponse
from app.infraestructure.service import classifier_service
from app.infraestructure.db.db import get_db
from app.domain.use_cases import get_message_tags
from app.infraestructure.dependencies import get_current_user

logger = logging.getLogger("uvicorn.error")

router = APIRouter()

@router.post("/tag-message", response_model=TagResponse)
async def tag_message(request: TagRequest, 
                db=Depends(get_db),
                user_id=Depends(get_current_user)):

    from_user_ids = await get_message_tags(db,user_id,request.text)
    to_user_ids = await get_message_tags(db,request.to_user_id,request.text)


    return TagResponse(to_user_tags=to_user_ids, from_user_tags=from_user_ids)