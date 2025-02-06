from pydantic import BaseModel, ConfigDict, computed_field
from datetime import datetime
from typing import Optional
from .roles import RoleModel


class UserBase(BaseModel):
    email: str
    firstname: str
    lastname: Optional[str]
    username: Optional[str] = None
    password: Optional[str] = None
    avatar_url: Optional[str] = None


class UserModel(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_time: datetime
    username_last_changed: Optional[datetime] = None
    roles: list[RoleModel]  # Represent roles as nested objects

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.firstname} {self.lastname}" if self.lastname else self.firstname


class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    avatar_url: Optional[str] = None


class UserProfile(BaseModel):
    email: str
    firstname: str
    lastname: Optional[str]
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    roles: list[str]
    full_name: str
