from domain.message_domain import DomainMessage
from services.tagging_api import request_tags
from infra.repository.message_repository import save_message

async def send_message(db, msg_in_schema):
    # 1. Instancia el dominio a partir del schema de entrada
    domain_msg = DomainMessage(
        from_user=msg_in_schema.from_user,
        to_user=msg_in_schema.to_user,
        content=msg_in_schema.content
    )

    # 2. Llama a la api de etiquetado y añade las etiquetas
    domain_msg.tags = await request_tags(domain_msg.content)

    # 3. Guarda el mensaje y sus tags en la base de datos
    db_msg, tag_objs = save_message(db, domain_msg)

    return domain_msg, db_msg, tag_objs