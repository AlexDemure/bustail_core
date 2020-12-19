from pydantic import BaseModel
from decimal import Decimal


class DriverBase(BaseModel):
    license_number: str = None


class DriverCreate(DriverBase):
    account_id: int
    debt: Decimal = Decimal("0")


class DriverData(DriverBase):
    id: int
    account_id: int
