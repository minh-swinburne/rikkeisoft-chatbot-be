from pydantic import BaseModel, ConfigDict, model_validator
from datetime import datetime
from typing import Optional, Self
from .roles import RoleModel


class UserBase(BaseModel):
    email: str
    firstname: str
    lastname: Optional[str]
    username: Optional[str] = None
    password: Optional[str] = None
    avatar_url: Optional[str] = None


class UserModel(UserBase):
    id: str
    created_time: datetime
    username_last_changed: Optional[datetime] = None
    roles: list[RoleModel]  # Represent roles as nested objects

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    avatar_url: Optional[str] = None
    roles: Optional[list[int]] = None  # Allow updating roles by ID
