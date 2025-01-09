from pydantic import BaseModel
from datetime import datetime

class ChatBase(BaseModel):
    name: str

class ChatResponse(ChatBase):
    id: int
    user_id: int
    last_access: datetime
