from sqlalchemy import Column, Integer, String, DateTime, Boolean
from infraestructure.postgres.database import Base
import datetime

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, nullable=False)
    recipient = Column(String, nullable=False)
    content = Column(String, nullable=False)
    label = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    read = Column(Boolean, default=False)