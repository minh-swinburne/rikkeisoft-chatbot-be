from sqlalchemy import Column, String, Text, Boolean, Date, DateTime
from sqlalchemy.sql import func
from app.models.base import Base


class DocumentBase(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    categories = Column(String(255), nullable=False)  # Stored as comma-separated values
    creator = Column(String(36), nullable=False)  # ForeignKey to User table if needed
    created_date = Column(Date)
    restricted = Column(Boolean, nullable=False)
    uploader = Column(String(36), nullable=False)  # ForeignKey to User table if needed
    uploaded_time = Column(DateTime(timezone=True), server_default=func.now())
