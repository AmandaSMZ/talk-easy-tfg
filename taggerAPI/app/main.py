from fastapi import FastAPI
from models import TagRequest, TagResponse
from service import ZeroShotClassifierService
import logging


logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="SmartLabel API",
    description="Microservicio IA para etiquetado automático de mensajes (zero-shot classification)."
)

classifier_service = ZeroShotClassifierService()

@app.get("/")
def read_root():
    return {"message": "API de etiquetado automático de mensajes (zero-shot classification)"}

@app.post("/tag-message", response_model=TagResponse)

def tag_message(request: TagRequest):

    logger.info(f"Petición recibida: {request}")

    response = classifier_service.tag_message(request)

    logger.info(f"Respuesta enviada: {response}")

    return response