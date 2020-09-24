from datetime import datetime
from typing import List
from pydantic import BaseModel, constr, validator
from notifications.schemas import Notification
from applications.enums import ApplicationStatus, ApplicationTypes


class ApplicationBase(BaseModel):
    to_go_from: constr(min_length=1, max_length=255)
    to_go_to: constr(min_length=1, max_length=255)
    to_go_when: datetime
    count_seats: int = 1
    description: constr(min_length=1, max_length=1024)
    price: int = 0
    application_type: constr(min_length=1, max_length=64) = ApplicationTypes.other.value

    @validator('application_type')
    def check_type_enum(cls, value):
        assert ApplicationTypes(value), 'Value is not enum'
        return value


class ApplicationCreate(ApplicationBase):
    client_id: int
    expired_at: datetime
    application_status: constr(min_length=1, max_length=64) = ApplicationStatus.waiting.value

    @validator('application_status')
    def check_status_enum(cls, value):
        assert ApplicationStatus(value), 'Value is not enum'
        return value

    @validator('to_go_when', 'expired_at')
    def remove_tzinfo(cls, value):
        """
        Удаление timezone из разных часовых поясах.
        Для преобразование даты в единный формат.
        Если этого не делать будут исключения на уровне БД что разные часовые пояса.
        """
        value = value.replace(tzinfo=None)
        return value


class Application(ApplicationCreate):
    id: int
    driver_id: int = None
    created_at: datetime
    confirmed_at: datetime = None

    class Config:
        orm_mode = True


class ApplicationFilters(BaseModel):
    limit: int = 10
    offset: int = 0
    city: str = ""
    order_by: str = 'to_go_when'
    order_type: str = 'asc'


class ApplicationWithNotifications(Application):
    notifications: List[Notification]


class ClientApplications(BaseModel):
    actual_applications: List[ApplicationWithNotifications]
    completed_applications: List[Application]
