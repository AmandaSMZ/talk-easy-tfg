from typing import Optional
from fastapi import Request
from fastapi.responses import JSONResponse
import httpx

INTERNAL_TOKEN = "tu_token_super_secreto"

async def proxy_request(request: Request, base_url: str, user, data:Optional[None]):

    async with httpx.AsyncClient() as client:

        url = f"{base_url}{request.url.path}"
        headers = dict(request.headers)
        headers.pop("host", None)
        headers["x-user-id"] = user["id"]
        headers["x-username"] = user["username"]
        headers["X-Internal-Token"] = INTERNAL_TOKEN

        method = request.method

        resp = await client.request(
            method,
            url,
            headers=headers,
            content=data,
            params=dict(request.query_params)
        )

    return JSONResponse(content=resp.json(), status_code=resp.status_code)

