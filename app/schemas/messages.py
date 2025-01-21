from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MessageBase(BaseModel):
    chat_id: str
    role: str
    content: str


class MessageModel(MessageBase):
    id: str
    time: datetime

    model_config = ConfigDict(from_attributes=True)
