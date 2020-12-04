from typing import Optional
from app.enums import EnumRoles
from pydantic import BaseModel


# Shared properties
class AccountBase(BaseModel):
    full_name: str
    email: str
    password: str


# Properties to receive on item creation
class AccountCreate(BaseModel):
    full_name: str
    email: str
    hashed_password: str


# Properties to receive on item creation
class AccountUpdate(BaseModel):
    full_name: str


class AccountData(BaseModel):
    full_name: str
    email: str
    role: EnumRoles
