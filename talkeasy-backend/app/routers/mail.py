from fastapi import APIRouter, Depends
from app.auth.auth_bearer import JWTBearer

router = APIRouter(prefix="/mail", tags=["mail"])

@router.post("/receive", dependencies=[Depends(JWTBearer())])
async def receive_email(subject: str, body: str):
    return {"msg": "Correo recibido", "etiqueta": "importante"}
