from sqlalchemy import Column, String, Enum, Text, Date, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.models.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(
        Enum("pdf", "docx", "xlsx", "html", name="file_type_enum"), nullable=False
    )
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    categories = Column(String(255), nullable=False)
    creator = Column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_date = Column(Date, nullable=True)
    restricted = Column(Boolean, default=False, nullable=False)
    uploader = Column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    uploaded_time = Column(DateTime(timezone=True), server_default=func.now())
    last_modified = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )
