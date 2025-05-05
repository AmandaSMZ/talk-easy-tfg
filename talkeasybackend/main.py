from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from routes import auth_routes, messages_routes

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(messages_routes.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return 'Bienvenidos'

@app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")


