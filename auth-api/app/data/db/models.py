from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from app.data.db.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
        )
    email: Mapped[str] = mapped_column(
        String, unique=True, 
        index=True
        )
    hashed_password: Mapped[str] = mapped_column(
        String
        )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )