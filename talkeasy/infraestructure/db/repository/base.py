from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from domain.message_domain import DomainMessage

class IMessageRepository(ABC):

    @abstractmethod
    async def save_message(self, message: DomainMessage) -> DomainMessage:
        pass

    @abstractmethod
    async def get_messages_by_chat(self, user1: UUID, user2: UUID, last_id: Optional[UUID] = None) -> List[DomainMessage]:
        pass

    @abstractmethod
    async def get_messages_by_tag(self, user_id: UUID, tag_id: UUID) -> List[DomainMessage]:
        pass

    @abstractmethod
    async def list_conversations(self, user_id: UUID) -> List[UUID]:
        pass

    @abstractmethod
    async def create_conversation_if_not_exists(self, user1: UUID, user2: UUID) -> None:
        pass
