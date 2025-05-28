from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from infraestructure.db.base import Base
from datetime import datetime
import uuid
from sqlalchemy.orm import relationship

class MessageModel(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    to_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())
    is_read: Mapped[bool | None] = mapped_column(nullable=True)
    
    message_tags = relationship("MessageTagUserModel", back_populates="message")

class MessageTagUserModel(Base):
    __tablename__ = "message_tags"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("messages.id"), nullable=False)
    tag_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    message = relationship("MessageModel", back_populates="message_tags")

class Conversation(Base):
    __tablename__ = "conversations"

    user1_id = mapped_column(UUID(as_uuid=True), primary_key=True)
    user2_id = mapped_column(UUID(as_uuid=True), primary_key=True)