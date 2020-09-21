from sqlalchemy import select
from typing import Optional
from common.service import BaseService
from common.crud import create_object_model
from notifications import models, schemas
from db.database import database


class ServiceNotifications(BaseService):

    async def create(self) -> int:
        assert isinstance(self.schema, schemas.NotificationCreate), 'Schema is wrong format'
        return await create_object_model(models.notifications, self.schema.dict())

    @staticmethod
    async def get_notifications_by_application_and_transport(
            application_id: int,
            transport_id: int,
            decision: bool = None
    ) -> Optional[dict]:
        query = (
            select([models.notifications])
            .where(
                (models.notifications.c.application_id == application_id) &
                (models.notifications.c.transport_id == transport_id) &
                (models.notifications.c.decision == decision)
            )
        )
        notification = await database.fetch_one(query)
        return dict(notification) if notification else None
