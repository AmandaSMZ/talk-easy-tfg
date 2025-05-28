import httpx

TAGGING_API_URL = "http://tagging-api:8003/tags/available"

async def request_tags(text: str, tags: list[str]) -> list[str]:
    payload = {
        "text": text,
        "labels": tags
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(TAGGING_API_URL, json=payload)
        response.raise_for_status()
        if not response.text:
            return []

        try:
            return response.json().get("predicted_labels", [])
        
        except ValueError:
            return []


'''
async def get_available_tags() -> list[str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TALKEASY_API_URL}/tags/available")
        response.raise_for_status()
        return response.json()
        
'''