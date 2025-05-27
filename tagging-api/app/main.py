from fastapi import FastAPI
from app.api.routes.tag_routes import router as tag_router
from app.api.routes.service_routes import router as serv_router

app = FastAPI(
    title="Tagging API",
    description="Microservicio IA para etiquetado automático de mensajes (zero-shot classification)."
)

app.include_router(tag_router)

app.include_router(serv_router)

@app.get("/")
def read_root():
    return {"message": "API de etiquetado automático de mensajes (zero-shot classification)"}

