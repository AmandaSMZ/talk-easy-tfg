from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime


class Tag(BaseModel):
    id: str
    name: Optional[str] = None

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    text: str


class MessageIn(MessageBase):
    to_user_id: str
    from_user_tags: Optional[List[Tag]] = None
    to_user_tags: Optional[List[Tag]] = None


class MessageOut(MessageBase):
    id: str
    with_user_id: Optional[str] = None
    timestamp: datetime
    type: Literal["sent", "received"]
    tags: Optional[List[Tag]] = None

    class Config:
        orm_mode = True
