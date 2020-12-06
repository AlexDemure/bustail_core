from pydantic import BaseModel


class AccountBase(BaseModel):
    fullname: str
    phone: str
    city: str


class AccountCreate(AccountBase):
    hashed_password: str


class AccountUpdate(AccountBase):
    pass


class AccountData(AccountBase):
    id: int

