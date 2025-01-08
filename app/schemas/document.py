from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class Document(BaseModel):
    id: Optional[str]
    filename: str
    file_type: str
    title: str
    description: Optional[str]
    categories: list[str]
    creator: str
    created_date: date
    restricted: bool
    uploader: str
    uploaded_date: datetime = datetime.now()
