from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

Base = declarative_base()

class Message(Base):

    id = Column(Integer, primary_key=True, index=True)
    from_user = Column(String, nullable=False) 
    to_user = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(datetime.timezone.utc))
    is_read = Column(Integer, default=0)


class MessageTag(Base):

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, nullable=False)
    tag = Column(String, nullable=False)