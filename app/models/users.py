from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, validates
from app.models.base import Base
import re


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=True)
    password = Column(String(60), nullable=True)  # Nullable for SSO accounts
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=True)  # Nullable to allow flexibility
    admin = Column(Boolean, default=False)
    username_last_changed = Column(DateTime, nullable=True)

    # Relationship to SSO accounts
    sso_accounts = relationship(
        "SSOAccount", back_populates="user", cascade="all, delete-orphan"
    )

    @validates("username")
    def validate_username(self, key, username):
        """
        Validates the username field for native accounts.
        - Must be non-empty, start with a letter, and only contain alphanumeric or underscores.
        - Optional for SSO users.
        """
        if username:
            if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", username):
                raise ValueError(
                    "Invalid username. Must start with a letter and contain only alphanumeric characters or underscores."
                )
        return username
