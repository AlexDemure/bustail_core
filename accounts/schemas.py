from pydantic import BaseModel, constr
from datetime import datetime, date


class PersonalDataBase(BaseModel):
    fullname: constr(max_length=255)
    phone: constr(max_length=12)
    email: constr(max_length=64) = None
    birthday: date = None
    city: constr(max_length=128)


class PersonalDataCreate(PersonalDataBase):
    account_id: int


class PersonalDataUpdate(PersonalDataCreate):
    pass


class PersonalData(PersonalDataCreate):

    class Config:
        orm_mode = True


class AuthorizationDataBase(BaseModel):
    login: str
    password: str


class AuthorizationDataCreate(AuthorizationDataBase):
    account_id: int


class AuthorizationDataUpdate(AuthorizationDataCreate):
    pass


class AuthorizationData(AuthorizationDataBase):

    class Config:
        orm_mode = True


class AccountCreate(BaseModel):
    authorization_data: AuthorizationDataBase
    personal_data: PersonalDataBase


class AccountDelete(BaseModel):
    account_id: int


class Account(AccountCreate):
    id: int
    registration_date: datetime

    class Config:
        orm_mode = True