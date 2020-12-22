from decimal import Decimal
from typing import List

from object_storage.enums import FileMimetypes
from pydantic import BaseModel, root_validator

from backend.common.utils import get_cities
from backend.drivers.enums import TransportType


class DriverBase(BaseModel):
    license_number: str = None


class DriverCreate(DriverBase):
    account_id: int
    debt: Decimal = Decimal("0")


class DriverData(DriverBase):
    id: int
    account_id: int


class TransportBase(BaseModel):
    transport_type: TransportType
    brand: str
    model: str
    count_seats: int = 1
    price: int = 0
    city: str
    state_number: str

    @root_validator
    def check_values(cls, values):
        if values['city'] not in get_cities():
            raise ValueError("City is not found")

        return values


class TransportUpdate(TransportBase):
    driver_id: int


class TransportCreate(TransportBase):
    driver_id: int


class TransportData(TransportBase):
    id: int
    driver_id: int


class ListTransports(BaseModel):
    transports: List[TransportData]


class TransportPhotoBase(BaseModel):
    transport_id: int
    file_uri: str
    file_hash: str
    media_type: FileMimetypes


class TransportPhotoCreate(TransportPhotoBase):
    pass


class TransportPhotoData(TransportPhotoBase):
    id: int
