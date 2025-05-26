import httpx
from fastapi import HTTPException, Header, status

AUTH_API_URL = "http://auth-api:8001/auth/me"

async def get_user_from_token(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(AUTH_API_URL, headers=headers)
    
    if resp.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return resp.json()

async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    token = authorization.split(" ")[1]
    user = await get_user_from_token(token)
    return user