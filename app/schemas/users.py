from pydantic import BaseModel
from typing import List, Optional


class UserBase(BaseModel):
    username: str
    email: str
    firstname: str = None
    lastname: str = None
    provider: Optional[str] = None
    provider_uid: Optional[str] = None


class UserCreate(UserBase):
    password: str  # Password is required when creating a user


class UserResponse(UserBase):
    id: str
    admin: bool
