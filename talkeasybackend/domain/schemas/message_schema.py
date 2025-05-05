from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    sender: str
    recipient: str
    content: str

class MessageResponse(BaseModel):
    id: int
    sender: str
    recipient: str
    content: str
    label: str
    timestamp: datetime
    read: bool

    model_config = { "from_attributes": True }