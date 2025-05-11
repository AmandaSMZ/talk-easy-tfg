from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageIn(BaseModel):
    from_user: str
    to_user: str
    content: str


class MessageOutSender(MessageIn):
    timestamp: datetime
    tags: Optional[list[str]] = None