from typing import List
from uuid import UUID

class DomainMessage:
    def __init__(self, from_user_id, to_user_id, content, timestamp=None, tags=None, is_read=False, id=None):
        self.id = id
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.content = content
        self.timestamp = timestamp
        self.tags : List[DomainTag] = tags or []
        self.is_read = is_read

class DomainTag:
    def __init__(self, name: str, id: UUID = None):
        self.id = id
        self.name = name