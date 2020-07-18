from datetime import datetime
from pydantic import BaseModel


class ClientBase(BaseModel):
    account_id: int


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
