from domain.schemas.message_schema import MessageCreate, MessageResponse
from infraestructure.postgres.repositories.message_repository import save_message
from infraestructure.ext_api.api_ia import get_label
from sqlalchemy.orm import Session

async def send_message_use_case(message: MessageCreate, db: Session) -> MessageResponse:
    # 1. Llama a la IA para etiquetar el mensaje
    label = await get_label(message.content)
    
    # 2. Guarda el mensaje usando la función repository
    saved_message = save_message(
        db=db,
        sender=message.sender,
        recipient=message.recipient,
        content=message.content,
        label=label
    )

    # 3. Devuelve la respuesta de acuerdo al esquema
    return MessageResponse.model_validate(saved_message)