from typing import Optional

from sqlalchemy import select

from common.service import BaseService
from common.crud import create_object_model, get_object_model
from db.database import database
from drivers import models, schemas


class ServiceDriver(BaseService):

    async def create(self) -> int:
        assert isinstance(self.schema, schemas.DriverDataCreate), 'Schema is wrong format'
        return await create_object_model(models.drivers, self.schema.dict())

    @staticmethod
    async def get_by_account_id(account_id: int) -> Optional[dict]:
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

    @staticmethod
    async def get(transport_id: int) -> Optional[dict]:
        return await get_object_model(models.transports, transport_id)

    @staticmethod
    async def get_driver_transports(driver_id: int) -> list:
        query = (
            select([models.transports])
            .where(models.transports.c.driver_id == driver_id)
        )
        transports = await database.fetch_all(query)
        return [dict(x) for x in transports]