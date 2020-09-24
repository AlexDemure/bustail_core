from sqlalchemy import select
from typing import Optional
from common.service import BaseService
from common.crud import create_object_model, get_object_model, update_object_model
from common.schemas import UpdateBase
from applications import schemas, models, enums
from db.database import database


class ServiceApplication(BaseService):

    async def create(self) -> int:
        assert isinstance(self.schema, schemas.ApplicationCreate), 'Schema is wrong format'
        return await create_object_model(models.applications, self.schema.dict())

    async def update(self):
        assert isinstance(self.schema, UpdateBase), 'Schema is wrong format'
        return await update_object_model(
            models.applications,
            object_id=self.schema.id,
            updated_fields=self.schema.updated_fields
        )

    @staticmethod
    async def get(application_id: int) -> Optional[dict]:
        return await get_object_model(models.applications, application_id)

    @staticmethod
    async def get_actual_applications(client_id: int) -> list:
        query = (
            select([models.applications])
            .where(
                (models.applications.c.client_id == client_id) &
                (models.applications.c.application_status == enums.ApplicationStatus.waiting.value)
            )
        )
        applications = await database.fetch_all(query)
        return [dict(x) for x in applications]

    async def get_all_applications(self):
        assert isinstance(self.schema, schemas.ApplicationFilters), 'Schema is wrong format'

        order_by_query = getattr(models.applications.c, self.schema.order_by)

        if self.schema.order_type == 'asc':
            order_by_query = order_by_query.asc()
        elif self.schema.order_type == 'desc':
            order_by_query = order_by_query.desc()
        else:
            raise ValueError("Order tyep wrong format")

        filter_query = (
            (
                    (models.applications.c.to_go_from.like(f"%{self.schema.city}%")) |
                    (models.applications.c.to_go_to.like(f"%{self.schema.city}%"))
            ) & (models.applications.c.application_status == enums.ApplicationStatus.waiting.value)
        )

        query = (
            select([models.applications])
            .where(filter_query)
            .order_by(order_by_query)
            .offset(self.schema.offset)
            .limit(self.schema.limit)
        )
        applications = await database.fetch_all(query)
        return [dict(x) for x in applications]

