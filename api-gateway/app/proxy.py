import json
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import httpx

async def proxy_request(request: Request, base_url: str):
    async with httpx.AsyncClient() as client:
        url = f"{base_url}{request.url.path}"
        print(f"Proxying to URL: {url}", flush=True)
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
    
async def proxy_request(request: Request, base_url: str):
    async with httpx.AsyncClient(follow_redirects=True) as client:  # Añadir follow_redirects
        url = f"{base_url}{request.url.path}"
        print(f"Proxying to URL: {url}")
        
        headers = dict(request.headers)
        headers.pop("host", None)
        method = request.method
        req_data = await request.body()

        try:
            resp = await client.request(
                method,
                url,
                headers=headers,
                content=req_data,
                params=dict(request.query_params)
            )


            if resp.headers.get("content-type", "").startswith("application/json"):
                return JSONResponse(
                    content=resp.json(),
                    status_code=resp.status_code
                )
            else:
                return Response(
                    content=resp.content,
                    status_code=resp.status_code,
                    headers=dict(resp.headers)
                )
                
        except json.JSONDecodeError:
            return Response(
                content=resp.content,
                status_code=resp.status_code,
                headers=dict(resp.headers)
            )