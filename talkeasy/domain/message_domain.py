from dataclasses import dataclass
from typing import List
from uuid import UUID

@dataclass
class DomainMessage:
    def __init__(self, from_user_id, to_user_id, text, timestamp=None,from_user_tags=None, to_user_tags=None, is_read=False, id=None):
        self.id = id
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.text = text
        self.timestamp = timestamp
        self.to_user_tags : List[UUID] = to_user_tags or []
        self.from_user_tags : List[UUID] = from_user_tags or []
        self.is_read = is_read


@dataclass
class DomainConversation:
    def __init__(self, with_user:UUID):
        self.with_user = with_user