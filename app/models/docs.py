from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    Date,
    Boolean,
    DateTime,
    ForeignKey,
    Table,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

# Association table for many-to-many relationship between documents and categories
document_categories = Table(
    "document_categories",
    Base.metadata,
    Column(
        "document_id",
        String(36),
        ForeignKey("documents.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "category_id",
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relationship to Document
    documents = relationship(
        "Document", secondary=document_categories, back_populates="categories"
    )


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(
        Enum("pdf", "docx", "xlsx", "html", name="file_type_enum"), nullable=False
    )
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
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

    # Many-to-many relationship with Category
    categories = relationship(
        "Category",
        secondary=document_categories,
        back_populates="documents",
        lazy="joined",
    )
