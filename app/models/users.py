from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DATETIME
from sqlalchemy.orm import relationship
from app.models.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    admin = Column(Boolean, default=False)
    provider = Column(String(50))
    provider_uid = Column(String(100))

    chats = relationship("Chat", back_populates="user")