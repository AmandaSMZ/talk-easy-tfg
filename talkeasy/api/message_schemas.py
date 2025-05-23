from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageIn(BaseModel):
    to_user_id: UUID
    content: str


class MessageOutSender(BaseModel):
    content: str
    timestamp: datetime
    tags: Optional[list[str]] = None


class MessageOut(MessageIn):
    id: UUID
    timestamp: datetime
    tags: Optional[list[str]] = None

class TagIn(BaseModel):
    name: str

class TagsIn(BaseModel):
    tags: List[TagIn]