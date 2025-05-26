from fastapi import FastAPI, HTTPException, Request
import os
from dotenv import load_dotenv
import httpx
from app.proxy import proxy_request

load_dotenv()

AUTH_API_URL = os.getenv('AUTH_API_URL')
#TALKEASY_API_URL = os.getenv('TALKEASY_API_URL')

app = FastAPI(title="API Gateway", version="1.0")

PUBLIC_ROUTES = [
    "/auth/register",
    "/auth/login",
]

async def verify_token(request: Request):

    if request.url.path in PUBLIC_ROUTES:
        return True
    
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        async with httpx.AsyncClient() as client:
            verify_response = await client.get(
                f"{AUTH_API_URL}/auth/me",
                headers={"Authorization": auth_header}
            )

            if verify_response.status_code == 401:
                raise HTTPException(
                    status_code=401,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            elif verify_response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )
            
            elif verify_response.status_code != 200:
                raise HTTPException(
                    status_code=verify_response.status_code,
                    detail="Authentication service error"
                )
            
            return verify_response

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail="Error validating token with authentication service"
        )

@app.api_route("/auth/{path:path}", methods=["GET", "POST"])
async def auth_proxy(request: Request):
    
    if request.url.path not in PUBLIC_ROUTES:
        user_info = await verify_token(request)
        if not user_info:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )
           
    return await proxy_request(request, base_url=AUTH_API_URL)