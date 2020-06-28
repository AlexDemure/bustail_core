from pydantic import BaseModel


class AccountBase(BaseModel):
    login: str
    password: str


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int

    class Config:
        orm_mode = True


class PersonBase(BaseModel):
    fullname: str
    phone: str


class PersonCreate(PersonBase):
    pass


class Person(PersonBase):
    id: int
    account_id: int

    class Config:
        orm_mode = True
