from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, Literal
from .categories import CategoryModel


class DocumentStatusModel(BaseModel):
    document_id: str
    uploaded: Literal["pending", "processing", "complete", "error"]
    embedded: Literal["pending", "processing", "complete", "error"]

    model_config = ConfigDict(from_attributes=True)


class DocumentBase(BaseModel):
    filename: str
    file_type: Literal["pdf", "docx", "xlsx", "html"]
    url: Optional[str]
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
    status: Optional[DocumentStatusModel]

    model_config = ConfigDict(from_attributes=True)


class DocumentUpdate(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    categories: Optional[list[int]] = None  # Allow updating categories by ID
    restricted: Optional[bool] = None
