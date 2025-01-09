from pydantic import BaseModel
from datetime import datetime

class MessageRequest(BaseModel):
    query: str

class MessageResponse(BaseModel):
    id: str
    chat_id: str
    time: datetime
    role: str
    content: str
