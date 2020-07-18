from pydantic import BaseModel


class AuthToken(BaseModel):
    access_token: str
    token_type: str


class AuthTokenData(BaseModel):
    account_id: int


class ClientCardToken(AuthToken):
    pass


class ClientCardTokenData(BaseModel):
    client_id: int
