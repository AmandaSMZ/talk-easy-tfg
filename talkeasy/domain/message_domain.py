from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID
from datetime import datetime

@dataclass
class DomainTag:
    id: UUID
    name: str

@dataclass
class DomainMessage:
    id: Optional[UUID]
    from_user_id: UUID
    to_user_id: UUID
    text: str
    timestamp: Optional[datetime]
    from_user_tags: Optional[List[DomainTag]]
    to_user_tags: Optional[List[DomainTag]]
    is_read: bool = False


@dataclass
class DomainConversation:
    def __init__(self, with_user:UUID):
        self.with_user = with_user