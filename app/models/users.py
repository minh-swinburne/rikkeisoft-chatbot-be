from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.models.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(String(255), primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    admin = Column(Boolean, default=False)
    provider = Column(String(50))
    providerUid = Column(String(100))

    chats = relationship("Chat", back_populates="user")