from datetime import datetime
from pydantic import BaseModel


class ClientBase(BaseModel):
    phone: str


class ClientCreate(BaseModel):
    person_id: int


class Client(ClientCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
