from pydantic import BaseModel


class DriverBase(BaseModel):
    license_number: str = None


class DriverCreate(DriverBase):
    pass


class DriverData(DriverBase):
    id: int
    account_id: int
