from pydantic import BaseModel, root_validator

from backend.common.utils import get_cities


class AccountBase(BaseModel):
    email: str
    city: str = None


class AccountCreate(AccountBase):
    hashed_password: str

    @root_validator
    def check_values(cls, values):
        if values['city'] not in get_cities():
            raise ValueError("City is not found")

        return values


class AccountUpdate(BaseModel):
    phone: str = None
    fullname: str = None
    city: str

    @root_validator
    def check_values(cls, values):
        phone = values.get('phone', None)
        fullname = values.get("fullname", None)

        if phone is None and fullname is None:
            raise ValueError("One of the values ​​must be specified")

        if values['city'] not in get_cities():
            raise ValueError("City is not found")

        return values


class AccountData(AccountBase):
    id: int
    fullname: str = None
    phone: str = None


class ConfirmAccount(BaseModel):
    code: str


class ChangePassword(BaseModel):
    password: str
