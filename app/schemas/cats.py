from pydantic import BaseModel, ConfigDict
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryModel(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
