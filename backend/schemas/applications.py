from datetime import date, datetime
from typing import List

from pydantic import BaseModel, constr, validator

from backend.enums.applications import ApplicationStatus, ApplicationTypes, ApplicationErrors
from backend.schemas.notifications import NotificationData


class ApplicationBase(BaseModel):
    to_go_from: constr(min_length=1, max_length=255)
    to_go_to: constr(min_length=1, max_length=255) = None
    to_go_when: date
    count_seats: int = 1
    description: constr(min_length=1, max_length=1024) = None
    price: int = 0
    application_type: ApplicationTypes = ApplicationTypes.other.value
    application_status: ApplicationStatus = ApplicationStatus.waiting.value

    @validator('to_go_when')
    def check_to_go_when_is_expired(cls, value):
        assert value >= datetime.utcnow().date(), ApplicationErrors.to_go_when_wrong_format.value
        return value


class ApplicationCreate(ApplicationBase):
    account_id: int


class ApplicationData(ApplicationBase):
    id: int
    account_id: int
    driver_id: int = None
    to_go_when: date = None
    created_at: datetime
    confirmed_at: datetime = None
    notifications: List[NotificationData] = None


class ListApplications(BaseModel):
    applications: List[ApplicationData]
