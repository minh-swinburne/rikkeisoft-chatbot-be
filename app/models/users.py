from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DATETIME
from sqlalchemy.orm import relationship, validates
from app.models.base import Base
import re

class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    admin = Column(Boolean, default=False)
    provider = Column(String(50))
    provider_uid = Column(String(100))

    chats = relationship("Chat", back_populates="user")

    @validates("username")
    def validate_username(self, key, username):
        if self.provider == "native":
            if not username:
                raise ValueError("Username is required for native users.")
            if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", username):
                raise ValueError(
                    "Invalid username. Must start with a letter and contain only alphanumeric characters or underscores."
                )
        elif username:  # For external providers
            raise ValueError("Username should not be set for external providers.")
        return username
