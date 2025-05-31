from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import httpx

timeout = httpx.Timeout(10.0, connect=5.0)

async def proxy_request(
    base_url: str,
    method: str,
    endpoint: str,
    expected_status_code: int,
    body: dict | None = None,
    headers: dict | None = None,
):
    headers = headers or {}
    async with httpx.AsyncClient(timeout=timeout) as client:
        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        if method.upper() == "GET":
            response = await client.get(url, headers=headers)
        elif method.upper() == "POST":
            response = await client.post(url, json=body, headers=headers)
        elif method.upper() =='DELETE':
            response = await client.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

    if response.status_code != expected_status_code:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return JSONResponse(content=response.json(), status_code=response.status_code)
