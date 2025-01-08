from pydantic import BaseModel


class MessageRequest(BaseModel):
    query: str


class MessageResponse(BaseModel):
    role: str
    content: str
