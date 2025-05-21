from fastapi import FastAPI
from api.message_routes import router as message_router
from api.ws_routes import ws_router

app = FastAPI()

app.include_router(message_router, prefix="/messages", tags=["mensaje"])

app.include_router(ws_router)
