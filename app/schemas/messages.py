from pydantic import BaseModel
from datetime import datetime


class MessageBase(BaseModel):
    chat_id: str
    role: str
    content: str


class MessageModel(MessageBase):
    id: str
    time: datetime