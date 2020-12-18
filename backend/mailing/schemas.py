from pydantic import BaseModel, EmailStr


class BaseEmail(BaseModel):
    email: EmailStr


class SendVerifyCodeEvent(BaseEmail):
    verify_code: str


class SendVerifyCodeEventCreate(BaseModel):
    account_id: int
    verify_code: str


class ChanePassword(BaseEmail):
    security_token: str
