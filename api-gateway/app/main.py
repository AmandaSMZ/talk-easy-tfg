from fastapi import FastAPI

from app.api.auth_routes import router as auth_router
from app.api.message_routes import router as msg_router
from app.api.tag_routes import router as tag_router

app = FastAPI(title="API Gateway", version="1.0")

app.include_router(auth_router)

app.include_router(msg_router)

app.include_router(tag_router)








