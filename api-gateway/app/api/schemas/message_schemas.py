from typing import List, Literal, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID
from app.api.schemas.user_schemas import UserSearch

class TagIn(BaseModel):
    name: str

class Tag(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    text: str

class MessageIn(MessageBase):
    to_user_id: str
    from_user_tags: Optional[List[Tag]] = None
    to_user_tags: Optional[List[Tag]] = None

class MessageOut(MessageBase):
    id: UUID
    timestamp: datetime
    with_user : UserSearch
    type: Literal["sent", "received"]
    tags: Optional[List[Tag]] = None

    class Config:
        orm_mode = True

