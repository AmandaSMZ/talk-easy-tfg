from fastapi import APIRouter, FastAPI, Request, Response, HTTPException
import httpx

router = APIRouter()

AUTH_API_URL = "http://auth-api:8000"
INTERNAL_TOKEN = "tu_token_super_secreto"
PUBLIC_ROUTES = [
    "/messages/login",
    "/messages/register"
]
client = httpx.AsyncClient()

async def proxy_to_auth(request: Request):
    url = AUTH_API_URL + request.url.path
    if request.url.query:
        url += "?" + request.url.query

    headers = dict(request.headers)
    headers.pop("host", None)

    body = await request.body()

    try:
        resp = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
            timeout=10.0
        )
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Error connecting to auth-api: {e}")

    return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)

@app.api_route("/register", methods=["POST"])
@app.api_route("/login", methods=["POST"])
@app.api_route("/me", methods=["GET"])
@app.api_route("/users/search/{email}", methods=["GET"])
async def auth_gateway(request: Request):
    return await proxy_to_auth(request)
