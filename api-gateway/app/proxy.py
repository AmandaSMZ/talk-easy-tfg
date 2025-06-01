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
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    headers = headers or {}
    method_upper = method.upper()

    async with httpx.AsyncClient(timeout=timeout) as client:
        
        if method_upper == "GET":
            response = await client.get(url, headers=headers)
        elif method_upper == "POST":
            response = await client.post(url, json=body, headers=headers)
        elif method_upper =='DELETE':
            response = await client.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method_upper}")

    if response.status_code != expected_status_code:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    try:
        content = response.json()
    except ValueError:
        content = response.text

    return content

    return JSONResponse(content=content, status_code=response.status_code)
