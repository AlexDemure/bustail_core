from datetime import datetime
from typing import List

from pydantic import BaseModel, constr, validator

from backend.applications.enums import ApplicationStatus, ApplicationTypes, ApplicationErrors


class ApplicationBase(BaseModel):
    to_go_from: constr(min_length=1, max_length=255)
    to_go_to: constr(min_length=1, max_length=255) = None
    to_go_when: str
    count_seats: int = 1
    description: constr(min_length=1, max_length=1024) = None
    price: int = 0
    application_type: ApplicationTypes = ApplicationTypes.other.value
    application_status: ApplicationStatus = ApplicationStatus.waiting.value


class ApplicationCreate(ApplicationBase):
    account_id: int
    to_go_when: datetime

    @validator('to_go_when')
    def check_to_go_when_is_expired(cls, value):
        assert value > datetime.utcnow(), ApplicationErrors.to_go_when_wrong_format.value
        return value


class ApplicationData(ApplicationBase):
    id: int
    account_id: int
    driver_id: int = None
    created_at: str
    confirmed_at: str = None


class ListApplications(BaseModel):
    applications: List[ApplicationData]
