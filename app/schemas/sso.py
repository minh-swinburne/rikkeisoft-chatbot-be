from pydantic import BaseModel, ConfigDict
from typing import Literal


class SSOModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    provider: Literal["google", "microsoft"]
    sub: str
    email: str
