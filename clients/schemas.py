from pydantic import BaseModel


class ClientDataCreate(BaseModel):
    account_id: int
