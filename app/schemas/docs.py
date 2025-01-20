from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, Literal
from .categories import CategoryModel


class DocumentBase(BaseModel):
    filename: str
    file_type: Literal["pdf", "docx", "xlsx", "html"]
    title: str
    description: Optional[str]
    categories: list[str]   # Allow categories to be passed as strings
    creator: str
    created_date: Optional[date]
    restricted: bool = False
    uploader: str


class DocumentModel(DocumentBase):
    id: str
    categories: list[CategoryModel] # Return categories as objects
    uploaded_time: datetime
    last_modified: datetime


class DocumentUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    categories: Optional[list[int]]  # Allow updating categories by ID
    restricted: Optional[bool]
