from pydantic import BaseModel
from datetime import datetime

class ChatBase(BaseModel):
    name: str
    user_id: str

class ChatResponse(ChatBase):
    id: str
    last_access: datetime
