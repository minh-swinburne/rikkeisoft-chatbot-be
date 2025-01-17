from pydantic import BaseModel
from datetime import datetime


class ChatBase(BaseModel):
    user_id: str
    name: str


class ChatModel(ChatBase):
    id: str
    last_access: datetime
