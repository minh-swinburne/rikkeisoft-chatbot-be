from pydantic import BaseModel


class GoogleAuthBase(BaseModel):
    access_token: str


class MicrosoftAuthBase(BaseModel):
    access_token: str
    id_token: str
