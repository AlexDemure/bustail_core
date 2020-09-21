from common.service import BaseService
from applications import schemas, models
from db.database import database


class ServiceApplication(BaseService):

    async def create(self) -> int:
        assert isinstance(self.schema, schemas.ApplicationCreate), 'Schema is wrong format'
        query = models.applications.insert().values(**self.schema.dict())
        application_id = await database.execute(query)
        return application_id
