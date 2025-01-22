from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, validates
from .base import Base
import re


# Association table for many-to-many relationship
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", String(36), ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    # Relationship with User
    users = relationship("User", secondary=user_roles, back_populates="roles")


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=True)  # Nullable to allow flexibility
    username = Column(String(50), nullable=True)
    password = Column(String(60), nullable=True)  # Nullable for SSO accounts
    avatar_url = Column(Text, nullable=True)
    created_time = Column(DateTime(timezone=True), nullable=False)
    username_last_changed = Column(DateTime(timezone=True), nullable=True)

    # Many-to-many relationship with Role
    roles = relationship(
        "Role", secondary=user_roles, back_populates="users", lazy="joined"
    )

    # One-to many relationship to SSO accounts
    sso = relationship("SSO", back_populates="user", cascade="all, delete-orphan")

    # One-to-many relationship to Chats
    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")

    @validates("username")
    def validate_username(self, key, username):
        """
        Validate the username field for native users.
        """
        if username:
            if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", username):
                raise ValueError(
                    "Invalid username. Must start with a letter and contain only alphanumeric characters or underscores."
                )
        return username
