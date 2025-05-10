import httpx

TAGGING_API_URL = "http://taggingAPI:8001/tag"  # Modifica el host/puerto real

async def request_tags(content: str) -> list[str]:
    async with httpx.AsyncClient() as client:
        response = await client.post(TAGGING_API_URL, json={"content": content})
        response.raise_for_status()
        return response.json().get("tags", [])