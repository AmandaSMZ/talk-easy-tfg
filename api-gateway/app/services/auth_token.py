from fastapi import FastAPI, HTTPException, Request
import os
from dotenv import load_dotenv
import httpx
from app.proxy import proxy_request
from app.api.auth_routes import AUTH_API_URL, PUBLIC_ROUTES


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
            detail=f"Authentication service unavailable: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error during authentication: {str(e)}"
        )