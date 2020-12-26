from pydantic import BaseModel, EmailStr


class BaseEmail(BaseModel):
    email: EmailStr


class SendVerifyCodeEvent(BaseEmail):
    message: str


class SendVerifyCodeEventCreate(BaseModel):
    account_id: int
    message: str


class ChangePassword(BaseEmail):
    message: str


class ChangePasswordEventCreate(BaseEmail):
    message: str
