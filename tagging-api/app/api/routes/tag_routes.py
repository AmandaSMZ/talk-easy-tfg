from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas import TagIn, Tag
from app.infraestructure.dependencies import get_current_user
from app.infraestructure.db.db import get_db
from app.domain.use_cases import create_tags_use_case, delete_tag_use_case, get_tags

router = APIRouter()

@router.post("/tags/add", 
        status_code=status.HTTP_201_CREATED,
        summary="Añade etiquetas posibles para el etiquetado de mensajes del usuario"
        )
async def create_tags_route(
    tags_in: List[TagIn],
    db: AsyncSession = Depends(get_db),
    user_id:UUID = Depends(get_current_user)
):
    if not tags_in:
        raise HTTPException(status_code=400, detail="La lista de etiquetas está vacía")
    
    return await create_tags_use_case(db, tags_in, user_id)


@router.get("/tags/available", 
        response_model=List[Tag],
        summary="Lista todas las etiquetas que tiene configuradas el usuario")
async def get_available_tags_route(
    db: AsyncSession = Depends(get_db),
    user_id:UUID = Depends(get_current_user)
    ):
    tags = await get_tags(db, user_id)
    if not tags:
        raise HTTPException(status_code=204, detail="Sin etiquetas configuradas")

    return tags

@router.delete("/tags/delete/{tag_id}",
        summary="Elimina la etiqueta que recibe por parámetro")
async def delete_tag(
    tag_id:UUID,
    db: AsyncSession = Depends(get_db),
    user_id:UUID = Depends(get_current_user)
    ):
    result = await delete_tag_use_case(db, tag_id, user_id)
    if result:
        return {"detail": "Etiqueta eliminada correctamente"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Etiqueta no encontrada o no pertenece al usuario"
        )