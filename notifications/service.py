from sqlalchemy import select
from typing import Optional, List
from common.service import BaseService
from common.crud import create_object_model, get_object_model, update_object_model
from common.schemas import UpdateBase
from notifications import models, schemas, enums
from db.database import database


class ServiceNotifications(BaseService):

    async def create(self) -> int:
        assert isinstance(self.schema, schemas.NotificationCreate), 'Schema is wrong format'
        return await create_object_model(models.notifications, self.schema.dict())

    async def update(self) -> None:
        assert isinstance(self.schema, UpdateBase), "Schema is wrong format"
        return await update_object_model(models.notifications, self.schema.id, self.schema.updated_fields)

    @staticmethod
    async def get(notification_id: int) -> Optional[dict]:
        return await get_object_model(models.notifications, notification_id)

    @staticmethod
    async def get_actual_by_application_id(application_id: int) -> List[dict]:
        query = (
            select([models.notifications])
            .where(
                (models.notifications.c.application_id == application_id) &
                (models.notifications.c.notification_type == enums.NotificationTypes.client.value) &
                (models.notifications.c.decision.is_(None))
            )
        )
        notification = await database.fetch_all(query)
        return [dict(x) for x in notification]

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
