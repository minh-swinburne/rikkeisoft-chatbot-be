from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, Literal
from .cats import CategoryModel
from .users import UserModel


class DocumentStatusBase(BaseModel):
    uploaded: Optional[Literal["pending", "processing", "complete", "error"]] = (
        "pending"
    )
    embedded: Optional[Literal["pending", "processing", "complete", "error"]] = (
        "pending"
    )


class DocumentStatusModel(DocumentStatusBase):
    model_config = ConfigDict(from_attributes=True)

    document_id: str


class DocumentBase(BaseModel):
    file_name: str
    file_type: Literal["pdf", "docx", "xlsx", "html"]
    link_url: Optional[str]
    title: str
    description: Optional[str]
    categories: list[str]  # Allow categories to be passed as strings
    creator: str
    created_date: Optional[date]
    restricted: bool
    uploader: str


class DocumentModel(DocumentBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    categories: list[CategoryModel]  # Return categories as objects
    creator_user: UserModel
    uploader_user: UserModel
    uploaded_time: datetime
    last_modified: datetime
    status: DocumentStatusModel


class DocumentUpdate(BaseModel):
    link_url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    categories: Optional[list[str]] = None  # Allow updating categories by ID
    restricted: Optional[bool] = None
    status: Optional[DocumentStatusBase] = None
