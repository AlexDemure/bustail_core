from pydantic import BaseModel, constr
from datetime import datetime, date


class AuthorizationDataBase(BaseModel):
    login: str
    password: str


class AuthorizationDataCreate(AuthorizationDataBase):
    account_id: int


class AuthorizationData(AuthorizationDataBase):

    class Config:
        orm_mode = True


class PersonalDataBase(BaseModel):
    fullname: constr(max_length=255)
    phone: constr(max_length=12)
    email: constr(max_length=64) = None
    birthday: date = None
    city: constr(max_length=128)


class PersonalDataCreate(PersonalDataBase):
    account_id: int


class PersonalData(PersonalDataCreate):

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    id: int
    registration_date: datetime

    class Config:
        orm_mode = True


class Account(AccountBase):
    authorization_data: AuthorizationDataBase = None
    personal_data: PersonalDataBase = None