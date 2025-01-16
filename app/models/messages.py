from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base


class Message(Base):
    __tablename__ = 'messages'

    id = Column(String(36), primary_key=True, index=True)
    chat_id = Column(String(36), ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    time = Column(DateTime(timezone=True), server_default=func.now())
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)

    chat = relationship("Chat", back_populates="messages")
