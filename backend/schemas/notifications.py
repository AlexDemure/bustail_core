from pydantic import BaseModel
from datetime import datetime

from backend.enums.notifications import NotificationTypes


class NotificationBase(BaseModel):
    application_id: int
    transport_id: int
    notification_type: NotificationTypes
    price: int = None


class NotificationCreate(NotificationBase):
    pass


class NotificationData(NotificationBase):
    id: int
    decision: bool = None
    created_at: datetime


class SetDecision(BaseModel):
    notification_id: int
    decision: bool
