from typing import Optional

from sqlalchemy import select

from common.service import BaseService
from common.crud import create_object_model
from db.database import database
from drivers import models, schemas


class ServiceDriver(BaseService):

    async def create(self) -> int:
        assert isinstance(self.schema, schemas.DriverDataCreate), 'Schema is wrong format'
        return await create_object_model(models.drivers, self.schema.dict())

    @staticmethod
    async def get(account_id: int) -> Optional[dict]:
        query = (
            select([models.drivers])
            .where(models.drivers.c.account_id == account_id)
        )
        driver_data = await database.fetch_one(query)
        return dict(driver_data) if driver_data else None


class ServiceTransport(BaseService):

    async def create(self) -> int:
        assert isinstance(self.schema, schemas.TransportCreate), 'Schema is wrong format'
        return await create_object_model(models.transports, self.schema.dict())
