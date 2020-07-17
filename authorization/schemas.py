from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    account_id: int


class AuthorizationDataBase(BaseModel):
    login: str
    password: str


class AuthorizationDataCreate(AuthorizationDataBase):
    account_id: int


class AuthorizationData(AuthorizationDataBase):

    class Config:
        orm_mode = True
