from typing import Optional

from pydantic import BaseModel, UUID4


class CredentialSchema(BaseModel):
    email: Optional[str]
    password: str

    class Config:
        schemas_extra = {"example": {"email": "my_email@gmail.com", "password": "qwerty"}}


class JWTToken(BaseModel):
    access_token: str
    token_type: str


class JWTTokenData(BaseModel):
    main: str = None


class JWTTokenPayload(BaseModel):
    user_uuid: UUID4 = None


class Msg:
    msg: str