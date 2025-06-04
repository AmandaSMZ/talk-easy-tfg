from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.auth_routes import router as auth_router
from app.api.message_routes import router as msg_router
from app.api.tag_routes import router as tag_router
from app.api.ws_routes import ws_router
from fastapi.middleware.cors import CORSMiddleware

class UTF8JSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"

app = FastAPI(title="API Gateway", version="1.0", default_response_class=UTF8JSONResponse)

origins = [

    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)

app.include_router(msg_router)

app.include_router(tag_router)

app.include_router(ws_router)








