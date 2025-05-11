from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from infraestructure.db.config import Base
from datetime import datetime, timezone

class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    from_user = Column(String, nullable=False)
    to_user = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_read = Column(Boolean, nullable=True)

class MessageTagModel(Base):
    __tablename__ = "message_tags"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)

class TagsModel(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)