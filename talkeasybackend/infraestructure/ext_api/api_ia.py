import httpx

AI_SERVICE_URL = "http://tagger-api:5000/tag-message"

CANDIDATE_LABELS = [
    "Trabajo",
    "Personal",
    "Formación",
    "Reunión",
    "Urgente"
]

async def get_label(text: str) -> str:
    payload = {
        "text": text,
        "labels": CANDIDATE_LABELS
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(AI_SERVICE_URL, json=payload)
        response.raise_for_status()
        return response.json()["label"]