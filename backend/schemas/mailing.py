from pydantic import BaseModel, EmailStr


class BaseEmail(BaseModel):
    email: EmailStr


class SendVerifyCodeEventCreate(BaseModel):
    account_id: int
    message: str


class ChangePasswordEventCreate(BaseEmail):
    message: str
