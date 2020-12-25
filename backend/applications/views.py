from fastapi import HTTPException
from datetime import datetime
from typing import Optional
from backend.applications import schemas, serializer, enums
from backend.applications.crud import application as application_crud
from backend.common.serializer import string_to_datetime
from backend.common.enums import BaseSystemErrors, BaseMessage
from backend.accounts.models import Account
from backend.common.schemas import UpdatedBase


async def create_application(account: Account, application_in: schemas.ApplicationBase) -> schemas.ApplicationData:
    """Создание заявки клиента."""
    assert isinstance(application_in, schemas.ApplicationBase), BaseSystemErrors.schema_wrong_format.value

    application_data = application_in.dict()

    if application_data.get("to_go_when"):
        to_go_when = string_to_datetime(application_data.pop("to_go_when"))
    else:
        to_go_when = None

    try:
        application_in = schemas.ApplicationCreate(
            account_id=account.id,
            to_go_when=to_go_when,
            **application_data
        )
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))

    application = await application_crud.create(application_in)
    return serializer.prepare_application(application)


async def get_all_applications(**kwargs) -> schemas.ListApplications:
    """
    Получение списка заявок клиента.

    Не относится к заявкам водителя.
    """
    applications = await application_crud.get_all_applications(**kwargs)
    return schemas.ListApplications(
        applications=[serializer.prepare_application(x) for x in applications]
    )


async def get_account_applications(account: Account) -> schemas.ListApplications:
    """
    Получение списка заявок клиента.

    Не относится к заявкам водителя.
    """
    applications = await application_crud.account_applications(account.id)
    return schemas.ListApplications(
        applications=[serializer.prepare_application(x) for x in applications]
    )


async def get_application(application_id: int) -> Optional[schemas.ApplicationData]:
    application = await application_crud.get(application_id)
    return serializer.prepare_application(application)


async def delete_application(account: Account, application_id: int) -> None:
    application = await application_crud.get(application_id)
    if not application:
        raise ValueError(BaseMessage.obj_is_not_found.value)

    assert application['account_id'] == account.id, enums.ApplicationErrors.application_does_not_belong_this_user.value

    await application_crud.remove(application['id'])

    application = await application_crud.get(application_id)
    assert application is None, "Application is not deleted"


async def confirmed_application(application_id: int, change_price: int = None) -> schemas.ApplicationData:
    application = await application_crud.get(application_id)
    if not application:
        raise ValueError(BaseMessage.obj_is_not_found.value)

    update_schema = UpdatedBase(
        id=application.id,
        updated_fields=dict(
            confirmed_at=datetime.utcnow(),
            price=change_price if change_price else application.price
        )
    )

    await application_crud.update(update_schema)

    return await application_crud.get(application.id)
