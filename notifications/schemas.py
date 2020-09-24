from datetime import datetime
from pydantic import BaseModel, constr, validator
from notifications.enums import NotificationTypes


class NotificationBase(BaseModel):
    application_id: int
    transport_id: int
    price: int = 0


class NotificationCreate(NotificationBase):
    notification_type: constr(min_length=1, max_length=64)

    @validator('notification_type')
    def check_notification_enum(cls, value):
        assert NotificationTypes(value), 'Value is not enum'
        return value


class Notification(NotificationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class NotificationDecision(BaseModel):
    id: int
    application_id: int
    transport_id: int
    decision: bool
    notification_type: constr(min_length=1, max_length=64)

    @validator('notification_type')
    def check_notification_enum(cls, value):
        assert NotificationTypes(value), 'Value is not enum'
        return value
