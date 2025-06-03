from fastapi import FastAPI
from api.message_routes import router as message_router

app = FastAPI()

app.include_router(message_router)

