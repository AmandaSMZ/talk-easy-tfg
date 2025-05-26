import httpx

TAGGING_API_URL = "http://tagging-api:8003/tags/available"
TALKEASY_API_URL = "http://talkeasy-api:8002"

async def request_tags(content: str, tags: list[str]) -> list[str]:
    payload = {
        "text": content,
        "labels": tags
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(TAGGING_API_URL, json=payload)
        response.raise_for_status()
        if not response.content:
            return []

        try:
            return response.json().get("predicted_labels", [])
        
        except ValueError:
            return []



async def get_available_tags() -> list[str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TALKEASY_API_URL}/tags/available")
        response.raise_for_status()
        return response.json()