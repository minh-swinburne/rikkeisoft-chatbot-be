from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class SSO(Base):
    __tablename__ = "sso"

    user_id = Column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    provider = Column(
        Enum("google", "microsoft", name="provider_enum"), primary_key=True
    )
    sub = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)

    user = relationship("User", back_populates="sso")
