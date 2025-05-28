from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Tag(BaseModel):
    id: UUID

class MessageIn(BaseModel):
    to_user_id: UUID
    text: str
    from_user_tags: Optional[List[UUID]] = None
    to_user_tags: Optional[List[UUID]] = None

class Message(BaseModel):
    id: Optional[UUID] = None
    from_user_id:Optional[UUID] = None
    timestamp: Optional[datetime] = None
    to_user_id: UUID
    text: str
    from_user_tags: Optional[List[UUID]] = None
    to_user_tags: Optional[List[UUID]] = None

class MessageSender(BaseModel):
    id: Optional[UUID]
    timestamp: Optional[datetime]
    to_user_id: UUID
    text: str
    from_user_tags: Optional[List[UUID]] = None

class MessageReceiver(BaseModel):
    id: Optional[UUID]
    from_user_id:Optional[UUID]
    timestamp: Optional[datetime]
    text: str
    to_user_tags: Optional[List[UUID]] = None
    

class Conversation(BaseModel):
    user_id: UUID