from fastapi import Request
from fastapi.responses import JSONResponse
import httpx

async def proxy_request(request: Request, base_url: str):
    async with httpx.AsyncClient() as client:
        url = f"{base_url}{request.url.path}"
        headers = dict(request.headers)
        headers.pop("host", None)
        method = request.method
        req_data = await request.body()

        resp = await client.request(
            method,
            url,
            headers=headers,
            content=req_data,
            params=dict(request.query_params)
        )

        return JSONResponse(content=resp.json(), status_code=resp.status_code)