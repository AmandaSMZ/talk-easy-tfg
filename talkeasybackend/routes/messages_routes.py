from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from domain.schemas.message_schema import MessageCreate, MessageResponse
from domain.use_cases.messages import send_message_use_case
from infraestructure.postgres.database import get_db

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/send", response_model=MessageResponse)
async def send_message_endpoint(
    message: MessageCreate,
    db: Session = Depends(get_db),
):
    try:
        return await send_message_use_case(message, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))