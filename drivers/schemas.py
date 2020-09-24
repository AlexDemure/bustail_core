from typing import List
from datetime import datetime
from pydantic import BaseModel, constr, validator, conint
from drivers.enum import TransportType
from notifications.schemas import Notification


class DriverDataCreate(BaseModel):
    account_id: int


class TransportBase(BaseModel):
    type_transport: constr(min_length=1, max_length=128) = TransportType.other.value
    brand: constr(min_length=1, max_length=255)
    model: constr(min_length=1, max_length=255)
    count_seats: conint(gt=0) = 1
    price: int = 0
    state_number: constr(min_length=1, max_length=64) = None
    city: constr(min_length=1, max_length=128)

    @validator('type_transport')
    def check_status_enum(cls, value):
        assert TransportType(value), 'Value is not enum'
        return value


class TransportCreate(TransportBase):
    driver_id: int


class Transport(TransportBase):
    id: int
    driver_id: int

    class Config:
        orm_mode = True


class TransportWithNotifications(Transport):
    notifications: List[Notification]


class TransportsWithNotifications(BaseModel):
    transports: List[TransportWithNotifications]


class TransportFilters(BaseModel):
    limit: int = 10
    offset: int = 0
    city: str = ""
    type_transport: str = None
    order_by: str = 'id'
    order_type: str = 'desc'

    @validator('type_transport')
    def check_status_enum(cls, value):
        if value is not None:
            assert TransportType(value), 'Value is not enum'
        return value
