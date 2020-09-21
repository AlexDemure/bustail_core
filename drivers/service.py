from typing import Optional

from sqlalchemy import select

from common.service import BaseService
from db.database import database
from drivers import models, schemas


class ServiceDriver(BaseService):

    async def create(self):
        assert isinstance(self.schema, schemas.DriverDataCreate), 'Schema is wrong format'
        query = models.drivers.insert().values(**self.schema.dict())
        driver_id = await database.execute(query)
        return driver_id

    @staticmethod
    async def get(account_id: int) -> Optional[dict]:
        query = (
            select([models.drivers])
            .where(models.drivers.c.account_id == account_id)
        )
        driver_data = await database.fetch_one(query)
        return dict(driver_data) if driver_data else None
