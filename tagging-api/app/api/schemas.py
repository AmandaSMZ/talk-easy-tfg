from uuid import UUID
from pydantic import BaseModel
from typing import List

class TagRequest(BaseModel):
    text: str
    to_user: UUID

class TagIn(BaseModel):
    name: str

class TagOut(BaseModel):
    id: UUID

class Tag(TagOut):
    name: str
    
class TagResponse(BaseModel):
    from_user_tags: List[TagOut]
    to_user_tags: List[TagOut]