from pydantic import BaseModel, root_validator


class AccountBase(BaseModel):
    email: str
    city: str = None


class AccountCreate(AccountBase):
    hashed_password: str


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

        return values


class AccountData(AccountBase):
    id: int
    fullname: str = None
    phone: str = None


class ConfirmAccount(BaseModel):
    code: str


class ChangePassword(BaseModel):
    password: str
