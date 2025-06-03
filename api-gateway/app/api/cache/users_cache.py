from typing import Dict, Optional
from uuid import UUID
from httpx import AsyncClient
from app.api.schemas.user_schemas import UserSearch
from fastapi import HTTPException


class UserCache:

    def __init__(self):
        self.cache: Dict[str, UserSearch] = {}
        self.api_url = "http://auth-api:8000"

    async def get_user(self, user_id: str, header) -> UserSearch:
        if not self.cache:
            await self.fetch_all_users(header) 

        if user_id in self.cache:
            return self.cache[user_id]

        user_data = await self.fetch_user_from_id(user_id, header)

        if user_data:
            user = UserSearch(**user_data)
            self.cache[user_id] = user
            return user
        else:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    async def fetch_user_from_id(self, user_id: str, header) -> Optional[dict]:
        async with AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/search/user-id", params={"id": user_id}, headers=header
            )
            if response.status_code == 200:
                data = response.json()
                if data:
                    return data[0]
            return None

    async def fetch_all_users(self, header: dict):
        async with AsyncClient() as client:
            response = await client.get(f"{self.api_url}/auth/search/", headers=header)
            if response.status_code == 200:
                data = response.json()
                if data:
                    for user_dict in data:
                        try:
                            user = UserSearch(**user_dict)
                            self.cache[user.id] = user
                        except Exception as e:
                            print(f"Error parsing user: {user_dict} - {e}")

user_cache = UserCache()