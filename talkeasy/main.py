from fastapi import FastAPI
from api.message_routes import router as message_routes

app = FastAPI()

app.include_router(message_routes, prefix="/messages", tags=["mensaje"])