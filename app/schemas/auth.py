from pydantic import BaseModel
from typing import Optional


class GoogleAuthBase(BaseModel):
    access_token: str


class MicrosoftAuthBase(BaseModel):
    access_token: str
    id_token: str


class TokenBase(BaseModel):
    sub: str
    email: str
    firstname: str
    lastname: Optional[str]
    username: Optional[str]
    avatar_url: Optional[str]
    provider: Optional[str]
    roles: list[str]


class TokenModel(TokenBase):
    type: str
    iat: int
    exp: int


class AuthModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
