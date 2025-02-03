from pydantic import BaseModel, ConfigDict
from typing import Optional


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


class RoleModel(RoleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
