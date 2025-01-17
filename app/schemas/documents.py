from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, Literal


class DocumentBase(BaseModel):
    filename: str
    file_type: Literal["pdf", "docx", "xlsx", "html"]
    title: str
    description: Optional[str]
    categories: str
    creator: str
    created_date: Optional[date]
    restricted: bool = Field(default=False)
    uploader: str


class DocumentModel(DocumentBase):
    id: str
    uploaded_time: datetime
    last_modified: datetime


class DocumentUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    categories: Optional[str]
    restricted: Optional[bool]
