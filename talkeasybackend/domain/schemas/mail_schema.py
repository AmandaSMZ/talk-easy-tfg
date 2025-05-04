from pydantic import BaseModel
from datetime import datetime

class MessageIn(BaseModel):
    content: str
    
class MessageOut(BaseModel):
    sender_mail: str
    content: str
    tag: str
    timestamp: datetime