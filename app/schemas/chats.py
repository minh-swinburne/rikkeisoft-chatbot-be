from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class ChatBase(BaseModel):
    user_id: str
    name: str


class ChatModel(ChatBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    last_access: datetime


class ChatUpdate(BaseModel):
    name: Optional[str] = None
    last_access: Optional[datetime] = None
