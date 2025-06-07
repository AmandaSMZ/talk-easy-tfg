from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.data.db.models import User
from app.api.schemas import UserCreate
from app.security.password import get_password_hash
from typing import List, Optional


class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id == user_id))

        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> User:
        existing_user = await self.get_user_by_email(user_data.email)
        if existing_user:
            return None

        hashed_pw = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username.capitalize(),
            email=user_data.email,
            hashed_password=hashed_pw
        )

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user

    async def search_users_by_email(self, email: Optional[str]) -> User:
        if email is None:
            result = await self.db.execute(select(User))
            return result.scalars().all()

        result = await self.db.execute(
                select(User).where(User.email.ilike(f"%{email}%")))

        return result.scalars().all()

    async def search_users_by_ids(self, user_ids: List[UUID]) -> list[User]:
        result = await self.db.execute(
            select(User).where(User.id.in_(user_ids))
        )
        return result.scalars().all()
