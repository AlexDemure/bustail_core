from datetime import datetime
from pydantic import BaseModel


class ApplicationBase(BaseModel):
    client_id: int
    to_go_from: str
    to_go_when: datetime
    count_seats: int


class ApplicationCreate(ApplicationBase):
    pass


class Application(ApplicationCreate):
    id: int
    phone: str

    class Config:
        orm_mode = True
