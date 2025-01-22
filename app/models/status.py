from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class DocumentStatus(Base):
    __tablename__ = "document_status"

    document_id = Column(
        String(36), ForeignKey("documents.id", ondelete="CASCADE"), primary_key=True
    )
    uploaded = Column(Enum("pending", "processing", "complete", "error", name="upload_status_enum"), default="pending")
    embedded = Column(Enum("pending", "processing", "complete", "error", name="embedded_status_enum"), default="pending")

    document = relationship("Document", back_populates="status", uselist=False)