from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageIn(BaseModel):
    id:int
    from_user: str
    to_user: str
    content: str


class MessageOutSender(BaseModel):
    content: str
    timestamp: datetime
    tags: Optional[list[str]] = None


class MessageOut(MessageIn):
    timestamp: datetime
    tags: Optional[list[str]] = None