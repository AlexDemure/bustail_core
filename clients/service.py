from typing import Optional
from sqlalchemy import select
from common.service import BaseService
from clients import models, schemas
from db.database import database


class ServiceClient(BaseService):

    async def create(self):
        assert isinstance(self.schema, schemas.ClientDataCreate), 'Schema is wrong format'
        query = models.clients.insert().values(**self.schema.dict())
        client_id = await database.execute(query)
        return client_id

    @staticmethod
    async def get(account_id: int) -> Optional[dict]:
        query = (
            select([models.clients])
            .where(models.clients.c.account_id == account_id)
        )
        client_data = await database.fetch_one(query)
        return dict(client_data) if client_data else None
