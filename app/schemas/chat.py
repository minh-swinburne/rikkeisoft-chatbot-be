from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    role: str
    content: str
