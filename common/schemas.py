from pydantic import BaseModel


class UpdateBase(BaseModel):
    id: int
    updated_fields: dict
