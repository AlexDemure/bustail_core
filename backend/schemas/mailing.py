from uuid import uuid4

from pydantic import BaseModel, EmailStr

from backend.mailing.settings import SERVICE_NAME


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


class MailingTask(BaseModel):
    task_id: str = str(uuid4())
    service_name: str = SERVICE_NAME
    message_type: str
    data: dict
