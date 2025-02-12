from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class MessageBase(BaseModel):
    chat_id: str
    role: str
    content: str
    summary: Optional[str] = None


class MessageModel(MessageBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    time: datetime
