from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .roles import RoleModel


class UserBase(BaseModel):
    email: str
    firstname: str
    lastname: Optional[str]
    username: Optional[str]
    password: Optional[str]
    avatar_url: Optional[str]


class UserModel(UserBase):
    id: str
    created_time: datetime
    username_last_changed: Optional[datetime] = None
    roles: list[RoleModel]  # Represent roles as nested objects


class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    avatar_url: Optional[str] = None
    roles: Optional[list[int]] = None  # Allow updating roles by ID
