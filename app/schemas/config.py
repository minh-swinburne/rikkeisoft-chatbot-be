from pydantic import BaseModel
from typing import Optional


class Config(BaseModel):
    config_name: str
    model: str
    max_tokens: int
    temperature: float
    system_prompt: str
    message_template: Optional[list[str]]

