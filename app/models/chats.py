from sqlalchemy import Column, String, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.models.base import Base

class Chat(Base):
    __tablename__ = 'chats'

    id = Column(String(255), primary_key=True, index=True)
    user_id = Column(String(255), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    last_access = Column(DATETIME, default='CURRENT_DATETIME')

    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat")
