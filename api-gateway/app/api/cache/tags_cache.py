from typing import Dict, Optional
from uuid import UUID
from httpx import AsyncClient
from fastapi import HTTPException
from app.api.schemas.message_schemas import Tag

class TagCache:
    def __init__(self):
        self.cache: Dict[str, Tag] = {}
        self.api_url = "http://tagging-api:8000"

    async def get_tag(self, tag_id: str, header: dict) -> Tag:
        if not self.cache:
            await self.fetch_all_tags(header)

        if tag_id in self.cache:
            return self.cache[tag_id]

        tag_data = await self.fetch_tag_from_id(tag_id, header)

        if tag_data:
            tag = Tag(**tag_data)
            self.cache[tag_id] = tag
            return tag
        else:
            raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")

    async def fetch_tag_from_id(self, tag_id: str, header: dict) -> Optional[dict]:
        async with AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/tags/{tag_id}", headers=header
            )
            if response.status_code == 200:
                return response.json()
            return None

    async def fetch_all_tags(self, header: dict):
        async with AsyncClient() as client:
            response = await client.get(f"{self.api_url}/tags/", headers=header)
            if response.status_code == 200:
                data = response.json()
                if data:
                    for tag_dict in data:
                        try:
                            tag = Tag(**tag_dict)
                            self.cache[tag.id] = tag
                        except Exception as e:
                            print(f"Error parsing tag: {tag_dict} - {e}")

tag_cache = TagCache()
