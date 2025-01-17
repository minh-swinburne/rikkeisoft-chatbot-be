from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: str
    firstname: str
    lastname: Optional[str]
    username: Optional[str]
    password: Optional[str]
    admin: bool = False


class UserModel(UserBase):
    id: str
    username_last_changed: datetime


class UserCreate(UserBase):
    password: str  # Password is required when creating a user


class UserResponse(UserBase):
    id: str
    admin: bool
