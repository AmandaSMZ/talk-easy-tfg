import httpx

TAGGING_API_URL = "http://tagging-api:8002/tag-message"

async def request_tags(content: str, tags: list[str]) -> list[str]:
    payload = {
        "text": content,
        "labels": tags

    }
    async with httpx.AsyncClient() as client:
        response = await client.post(TAGGING_API_URL, json=payload)
        response.raise_for_status()
        if response.status_code == 204 or not response.content:
            return []

        try:
            return response.json().get("predicted_labels", [])
        except ValueError:
            
            return []