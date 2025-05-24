from http.client import HTTPException
from fastapi import FastAPI, status
from app.api.routes import router


app = FastAPI(
    title="Auth API",
    version="1.0.0"
)

app.include_router(router, prefix="/auth", tags=["auth"])

@app.get("/health")

async def health_check():

    try:
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE , detail=str(e))