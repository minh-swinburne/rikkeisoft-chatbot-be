from pydantic import BaseModel


class GoogleAuthRequest(BaseModel):
    access_token: str


class MicrosoftAuthRequest(BaseModel):
    access_token: str
    id_token: str