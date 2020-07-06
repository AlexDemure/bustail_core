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


class PersonalDataBase(BaseModel):
    fullname: str
    phone: str


class PersonalDataCreate(PersonalDataBase):
    account_id: int


class Person(PersonalDataCreate):
    id: int

    class Config:
        orm_mode = True
