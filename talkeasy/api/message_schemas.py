from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Tag(BaseModel):
    id: UUID

class Message(BaseModel):
    to_user_id: UUID
    content: str
    tags: Optional[list[Tag]] = None
    
class MessageOut(Message):
    id: UUID
    from_user_id:UUID
    timestamp: datetime
    tags: Optional[List[Tag]] = None

class Conversation(BaseModel):
    id: UUID