from pydantic import BaseModel


class AccountBase(BaseModel):
    fullname: str
    phone: str
    email: str
    city: str = None


class AccountCreate(AccountBase):
    hashed_password: str


class AccountUpdate(AccountBase):
    pass


class AccountData(AccountBase):
    id: int


class ConfirmAccount(BaseModel):
    code: str
