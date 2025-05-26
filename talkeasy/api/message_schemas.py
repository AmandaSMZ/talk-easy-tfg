from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TagIn(BaseModel):
    name: str

class Tag(TagIn):
    id: UUID

class Tags(BaseModel):
    tags: List[Tag]

class Message(BaseModel):
    to_user_id: UUID
    content: str

class MessageIn(Message):
    tags: Optional[list[str]] = None

class MessageOut(Message):
    id: UUID
    timestamp: datetime
    tags: Optional[List[Tag]] = None

