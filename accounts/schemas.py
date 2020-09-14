from pydantic import BaseModel, constr, root_validator
from datetime import datetime, date


class PersonalDataBase(BaseModel):
    fullname: constr(max_length=255)
    phone: constr(max_length=12)
    email: constr(max_length=64) = None
    birthday: date = None
    city: constr(max_length=128)

    @root_validator
    def check_values(cls, values):
        assert len(values.get('fullname').split(' ')) == 3, \
            'Fullname is need have first name, last name and second name'

        return values


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


class ResetPasswordBase(BaseModel):
    login: str


class ResetPassword(ResetPasswordBase):
    password: str
    verify_code: str
