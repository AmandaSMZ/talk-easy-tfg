from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

class UserCredentials(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserCredentials):
    username: str

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

class MessageIn(BaseModel):
    to_user_id: str
    text: str
    from_user_tags: Optional[List[UUID]] = None
    to_user_tags: Optional[List[UUID]] = None

class TagIn(BaseModel):
    name: str

class Tag(TagIn):
    id: Optional[UUID]
