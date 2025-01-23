from pydantic import BaseModel, ConfigDict
from typing import Literal


class SSOModel(BaseModel):
    user_id: str
    provider: Literal["google", "microsoft"]
    sub: str

    model_config = ConfigDict(from_attributes=True)
    