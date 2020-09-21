from pydantic import BaseModel, constr, validator, conint
from drivers.enum import TransportType


class DriverDataCreate(BaseModel):
    account_id: int


class TransportBase(BaseModel):
    type_transport: constr(min_length=1, max_length=128) = TransportType.other.value
    brand: constr(min_length=1, max_length=255)
    model: constr(min_length=1, max_length=255)
    count_seats: conint(gt=0) = 1
    price: int = 0
    state_number: constr(min_length=1, max_length=64) = None

    @validator('type_transport')
    def check_status_enum(cls, value):
        assert TransportType(value), 'Value is not enum'
        return value


class TransportCreate(TransportBase):
    driver_id: int
