from typing import TypeVar
from uuid import uuid4
from pydantic import BaseModel

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class UpdatedBase(BaseModel):
    id: int
    updated_fields: dict


class Message(BaseModel):
    msg: str


class RedisTask(BaseModel):
    task_id: str = str(uuid4())
    service_name: str
    message_type: str
    data: dict
