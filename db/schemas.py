from pydantic import BaseModel
from datetime import datetime


class AccountBase(BaseModel):
    login: str


class AccountCreate(AccountBase):
    password: str


class Account(AccountCreate):
    id: int

    class Config:
        orm_mode = True


class PersonBase(BaseModel):
    fullname: str
    phone: str


class PersonCreate(PersonBase):
    account_id: int


class Person(PersonCreate):
    id: int

    class Config:
        orm_mode = True


class ClientBase(BaseModel):
    phone: str


class ClientCreate(BaseModel):
    person_id: int


class Client(ClientCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


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
