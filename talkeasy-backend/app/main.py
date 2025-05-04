from fastapi import FastAPI
from app.routers import mail

app = FastAPI()
app.include_router(mail.router)
