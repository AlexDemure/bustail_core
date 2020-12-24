from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import Response

from backend.applications import schemas, enums, views
from backend.common.deps import confirmed_account
from backend.common.schemas import Message
from backend.common.enums import BaseMessage
from backend.common.responses import auth_responses
from backend.accounts.models import Account

router = APIRouter()


@router.get(
    "/client/",
    response_model=schemas.ListApplications,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        **auth_responses
    }
)
async def get_account_applications(account: Account = Depends(confirmed_account)) -> schemas.ListApplications:
    """
    Получение списка заявок клиента.

    Не относится к заявкам водителя.
    """
    return await views.get_account_applications(account)


@router.get(
    "/driver/",
    response_model=schemas.ListApplications,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        **auth_responses
    }
)
async def get_driver_applications(account: dict = Depends(confirmed_account)) -> schemas.ListApplications:
    """
    Получение списка заявок водителя.

    Не относится к заявкам клиента.
    """
    pass


@router.post(
    "/",
    response_model=schemas.ApplicationData,
    responses={
        status.HTTP_201_CREATED: {"description": BaseMessage.obj_is_created.value},
        status.HTTP_400_BAD_REQUEST: {"description": BaseMessage.obj_is_not_created.value},
        **auth_responses
    }
)
async def create_application(
        application_in: schemas.ApplicationBase,
        response: Response,
        account: dict = Depends(confirmed_account),
):
    """Создание заявки."""
    try:
        app = await views.create_application(account, application_in)
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
async def get_application(application_id: int, account: dict = Depends(confirmed_account)):
    """Получение заявки клиента."""
    return await views.get_application(application_id)


@router.delete(
    "/{application_id}/",
    response_model=Message,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_is_deleted.value},
        status.HTTP_400_BAD_REQUEST: {"description": enums.ApplicationErrors.application_does_not_belong_this_user.value},
        **auth_responses
    }
)
async def delete_application(application_id: int, account: dict = Depends(confirmed_account)):
    """Удаление собственной заявки."""
    try:
        await views.delete_application(account, application_id)
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return Message(msg=BaseMessage.obj_is_deleted.value)


@router.get(
    "/",
    response_model=schemas.ListApplications,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        **auth_responses
    }
)
async def get_account_applications(
        limit: int = 10, offset: int = 0, city: str = "", order_by: str = 'to_go_when', order_type: str = 'asc'
) -> schemas.ListApplications:
    """Получение списка всех заявок."""

    query_params = dict(
        limit=limit, offset=offset, city=city, order_by=order_by, order_type=order_type
    )
    return await views.get_all_applications(**query_params)
