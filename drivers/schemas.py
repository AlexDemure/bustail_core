from pydantic import BaseModel


class DriverDataCreate(BaseModel):
    account_id: int
