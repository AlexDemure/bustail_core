from typing import Optional

from backend.applications.views import confirmed_application
from backend.common.enums import BaseSystemErrors, BaseMessage
from backend.common.schemas import UpdatedBase
from backend.notifications.crud import notification as notification_crud
from backend.enums.notifications import NotificationErrors
from backend.schemas.notifications import NotificationCreate, NotificationData
from backend.drivers.views import get_driver_by_transport_id


async def create_notification(notification_in: NotificationCreate) -> NotificationData:
    assert isinstance(notification_in, NotificationCreate), BaseSystemErrors.schema_wrong_format.value

    notification = await notification_crud.find_notification_without_decision(
        notification_in.application_id, notification_in.transport_id, notification_in.notification_type
    )
    if notification:
        raise ValueError(NotificationErrors.duplicate_notification.value)

    notification = await notification_crud.create(notification_in)
    return NotificationData(**notification.__dict__)


async def get_notification(notification_id: int) -> Optional[NotificationData]:
    notification = await notification_crud.get(notification_id)
    return NotificationData(**notification.__dict__) if notification else None


async def set_decision(notification_id: int, decision: bool) -> NotificationData:
    notification = await get_notification(notification_id)
    if not notification:
        raise ValueError(BaseMessage.obj_is_not_found.value)

    update_schema = UpdatedBase(
        id=notification.id,
        updated_fields=dict(decision=decision)
    )
    await notification_crud.update(update_schema)

    if decision is True:
        driver = await get_driver_by_transport_id(notification.transport_id)
        if not driver:
            raise ValueError(BaseMessage.obj_is_not_found.value)

        await confirmed_application(notification.application_id, driver.id, notification.price)

    return await get_notification(notification.id)
