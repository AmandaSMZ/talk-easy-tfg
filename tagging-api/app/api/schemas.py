from uuid import UUID
from pydantic import BaseModel
from typing import List

class TagRequest(BaseModel):
    text: str
    to_user_id: UUID

class TagIn(BaseModel):
    name: str

class Tag(TagIn):
    id: str
    
class TagResponse(BaseModel):
    from_user_tags: List[Tag]
    to_user_tags: List[Tag]