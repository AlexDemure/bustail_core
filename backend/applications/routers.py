from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import Response
from typing import List
from backend.accounts.models import Account
from backend.applications.views import (
    get_account_applications as view_get_account_applications,
    create_application as view_create_application,
    get_application as view_get_application,
    delete_application as view_delete_application,
    get_all_applications as view_get_all_applications,
    get_driver_applications as view_get_driver_applications,
)
from backend.common.deps import confirmed_account
from backend.common.enums import BaseMessage
from backend.common.responses import auth_responses
from backend.common.schemas import Message
from backend.enums.applications import ApplicationErrors
from backend.schemas.applications import ListApplications, ApplicationData, ApplicationBase
from backend.drivers.views import get_driver_by_account_id

router = APIRouter()


@router.get(
    "/client/",
    response_model=ListApplications,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        **auth_responses
    }
)
async def get_account_applications(account: Account = Depends(confirmed_account)) -> ListApplications:
    """
    Получение списка заявок клиента.

    Не относится к заявкам водителя.
    """
    return await view_get_account_applications(account)


@router.get(
    "/driver/",
    response_model=List[ApplicationData],
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        status.HTTP_404_NOT_FOUND: {"description": BaseMessage.obj_is_not_found.value},
        **auth_responses
    }
)
async def get_driver_applications(account: Account = Depends(confirmed_account)) -> List[ApplicationData]:
    """
    Получение списка заявок водителя.

    Не относится к заявкам клиента.
    """
    driver = await get_driver_by_account_id(account.id)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BaseMessage.obj_is_not_found.value
        )
    return await view_get_driver_applications(driver.id)


@router.post(
    "/",
    response_model=ApplicationData,
    responses={
        status.HTTP_201_CREATED: {"description": BaseMessage.obj_is_created.value},
        status.HTTP_400_BAD_REQUEST: {"description": BaseMessage.obj_is_not_created.value},
        **auth_responses
    }
)
async def create_application(
        application_in: ApplicationBase,
        response: Response,
        account: Account = Depends(confirmed_account),
):
    """Создание заявки."""
    try:
        app = await view_create_application(account, application_in)
        response.status_code = status.HTTP_201_CREATED
        return app

    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{application_id}/",
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        **auth_responses
    }
)
async def get_application(application_id: int, account: Account = Depends(confirmed_account)):
    """Получение заявки клиента."""
    return await view_get_application(application_id)


@router.put(
    "/{application_id}/",
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_is_changed.value},
        **auth_responses
    }
)
async def rejected_application(application_id: int, account: Account = Depends(confirmed_account)):
    """Отмена заявки."""
    try:
        await view_delete_application(account, application_id)
    except (AssertionError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    return Message(msg=BaseMessage.obj_is_changed.value)


@router.delete(
    "/{application_id}/",
    response_model=Message,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_is_deleted.value},
        status.HTTP_400_BAD_REQUEST:
            {"description": f"{ApplicationErrors.application_does_not_belong_this_user.value} or "
                            f"{ApplicationErrors.application_has_ended_status.value}"},
        **auth_responses
    }
)
async def delete_application(application_id: int, account: Account = Depends(confirmed_account)):
    """Удаление собственной заявки."""
    try:
        await view_delete_application(account, application_id)
    except (AssertionError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    return Message(msg=BaseMessage.obj_is_deleted.value)


@router.get(
    "/",
    response_model=ListApplications,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        **auth_responses
    }
)
async def get_all_applications(
        limit: int = 10, offset: int = 0, city: str = "", order_by: str = 'to_go_when', order_type: str = 'asc'
) -> ListApplications:
    """Получение списка всех заявок."""

    query_params = dict(
        limit=limit, offset=offset, city=city, order_by=order_by, order_type=order_type
    )
    return await view_get_all_applications(**query_params)
