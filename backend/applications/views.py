from datetime import datetime
from typing import Optional

from fastapi import HTTPException

from backend.accounts.models import Account
from backend.applications.crud import application as application_crud
from backend.applications.serializer import prepare_apps_with_notifications
from backend.common.enums import BaseSystemErrors, BaseMessage
from backend.common.schemas import UpdatedBase
from backend.drivers.crud import driver as driver_crud
from backend.enums.applications import ApplicationErrors, ApplicationStatus
from backend.schemas.applications import ApplicationBase, ApplicationData, ApplicationCreate, ListApplications


async def create_application(account: Account, application_in: ApplicationBase) -> ApplicationData:
    """Создание заявки клиента."""
    assert isinstance(application_in, ApplicationBase), BaseSystemErrors.schema_wrong_format.value

    application_data = application_in.dict()

    try:
        application_in = ApplicationCreate(
            account_id=account.id,
            **application_data
        )
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))

    application = await application_crud.create(application_in)
    return ApplicationData(**application.__dict__)


async def get_all_applications(**kwargs) -> ListApplications:
    """Получение списка всех заявок в системе с get-параметрами."""
    applications = await application_crud.get_all_applications(**kwargs)
    return ListApplications(
        applications=[ApplicationData(**x.__dict__) for x in applications]
    )


async def get_account_applications(account: Account) -> ListApplications:
    """
    Получение списка заявок клиента.

    Не относится к заявкам водителя.
    """
    applications = await application_crud.account_applications(account.id)
    return ListApplications(
        applications=[prepare_apps_with_notifications(x, x.notifications) for x in applications]
    )


async def get_driver_applications(driver_id: int) -> ListApplications:
    """
    Получение списка заявок водителя.

    Не относится к заявкам клиента.
    """
    applications = await application_crud.driver_applications(driver_id)
    return ListApplications(
        applications=[prepare_apps_with_notifications(x, []) for x in applications]
    )


async def get_application(application_id: int) -> Optional[ApplicationData]:
    application = await application_crud.get(application_id)
    return ApplicationData(**application.__dict__) if application else None


async def delete_application(account: Account, application_id: int) -> None:
    """Удаление заявки только в статусе ожидания."""
    application = await application_crud.get(application_id)
    if not application:
        raise ValueError(BaseMessage.obj_is_not_found.value)

    assert application.account_id == account.id, ApplicationErrors.application_does_not_belong_this_user.value
    assert application.application_status == ApplicationStatus.waiting, ApplicationErrors.application_has_ended_status.value

    await application_crud.remove(application['id'])

    application = await application_crud.get(application_id)
    assert application is None, "Application is not deleted"


async def confirm_application(application_id: int, driver_id: int, change_price: int = None) -> None:
    """Подтверждение заявки, происходит после того когда клиент или водитель приняк заявку."""
    application = await application_crud.get(application_id)
    if not application:
        raise ValueError(BaseMessage.obj_is_not_found.value)

    driver = await driver_crud.get(driver_id)
    if not driver:
        raise ValueError(BaseMessage.obj_is_not_found.value)

    update_schema = UpdatedBase(
        id=application.id,
        updated_fields=dict(
            confirmed_at=datetime.utcnow(),
            driver_id=driver_id,
            price=change_price if change_price else application.price,
            application_status=ApplicationStatus.confirmed
        )
    )

    await application_crud.update(update_schema)


async def reject_application(account: Account, application_id: int) -> None:
    """Отмена заявки."""
    application = await application_crud.get(application_id)
    if not application:
        raise ValueError(BaseMessage.obj_is_not_found.value)

    assert application.account_id == account.id, ApplicationErrors.application_does_not_belong_this_user.value
    assert application.application_status != ApplicationStatus.completed, ApplicationErrors.application_has_ended_status.value

    updated_schema = UpdatedBase(
        id=application.id,
        updated_fields=dict(application_status=ApplicationStatus.rejected)
    )
    await application_crud.update(updated_schema)

    application = await application_crud.get(application_id)
    assert application.application_status == ApplicationStatus.rejected, "Application is not rejected"
