from pydantic import BaseModel
from typing import Literal


class SSOBase(BaseModel):
    user_id: str
    provider: Literal["google", "microsoft"]
    sub: str