from datetime import datetime
from pydantic import BaseModel, constr, validator
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

    class Config:
        orm_mode = True
