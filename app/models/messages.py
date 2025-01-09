from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.models.base import Base

class Message(Base):
    __tablename__ = 'messages'

    id = Column(String(255), primary_key=True, index=True)
    chat_id = Column(String(255), ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    time = Column(DATETIME, default='CURRENT_DATETIME')
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)

    chat = relationship("Chat", back_populates="messages")