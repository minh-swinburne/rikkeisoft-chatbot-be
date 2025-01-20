from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ChatBase(BaseModel):
    user_id: str
    name: str


class ChatModel(ChatBase):
    id: str
    last_access: datetime


class ChatUpdate(BaseModel):
    name: Optional[str] = None
    last_access: Optional[datetime] = None
