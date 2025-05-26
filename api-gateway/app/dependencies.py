from fastapi import Request, HTTPException
import httpx
from app.config import AUTH_API_URL, PUBLIC_ROUTES

async def get_current_user(request: Request):
    if request.url.path in PUBLIC_ROUTES:
        return None

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"{AUTH_API_URL}/users/me",
                headers={"Authorization": auth_header},
                timeout=10.0
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Auth service unavailable: {str(e)}")

    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")

    return resp.json()
