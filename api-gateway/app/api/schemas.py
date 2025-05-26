from pydantic import BaseModel

class MessageIn(BaseModel):
    from_user: str
    to_user: str
    content: str