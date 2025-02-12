from pydantic import BaseModel
from typing import Optional


class ConfigParams(BaseModel):
    model: str
    max_tokens: int
    temperature: float
    top_p: float
    stop: Optional[str]
    stream: bool


class Config(BaseModel):
    model_options: list[str]
    params: ConfigParams
    system_prompt: str
    message_template: Optional[list[str]] = None
    length_limit: Optional[int] = None


class ConfigUpdate(BaseModel):
    system_prompt: str
    model: str
    max_tokens: int
    temperature: float
    stream: bool
    message_template: Optional[list[str]] = None
    length_limit: Optional[int] = None
