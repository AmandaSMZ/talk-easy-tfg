from app.infraestructure.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid

class TagModel(Base):
    __tablename__ = "tag"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),
                                          primary_key=True,
                                          default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),
                                               nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)