from sqlalchemy import select
from common.service import BaseService
from common.crud import create_object_model
from applications import schemas, models, enums
from db.database import database


class ServiceApplication(BaseService):

    async def create(self) -> int:
        assert isinstance(self.schema, schemas.ApplicationCreate), 'Schema is wrong format'
        return await create_object_model(models.applications, self.schema.dict())

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
