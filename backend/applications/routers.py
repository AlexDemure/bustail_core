from fastapi import APIRouter, Depends, status, HTTPException

from backend.applications import schemas, enums, views
from backend.common.deps import confirmed_account
from backend.common.responses import auth_responses

router = APIRouter()


@router.get(
    "/client/",
    response_model=schemas.ListApplications,
    responses={
        status.HTTP_200_OK: {"description": "Application list"},
        **auth_responses
    }
)
async def get_account_applications(account: dict = Depends(confirmed_account)) -> schemas.ListApplications:
    """
    Получение списка заявок клиента.

    Не относится к заявкам водителя.
    """
    return await views.get_account_applications(account)


@router.get(
    "/driver/",
    response_model=schemas.ListApplications,
    responses={
        status.HTTP_200_OK: {"description": "Application list"},
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
        status.HTTP_201_CREATED: {"description": "Application is created"},
        status.HTTP_400_BAD_REQUEST: {"description": enums.ApplicationErrors.to_go_when_wrong_format.value},
        **auth_responses
    }
)
async def create_application(application_in: schemas.ApplicationBase, account: dict = Depends(confirmed_account)):
    """Создание заявки."""
    try:
        return await views.create_application(account, application_in)
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{application_id}/",
    responses={
        status.HTTP_200_OK: {"description": "Application"},
        **auth_responses
    }
)
async def get_application(application_id: int, account: dict = Depends(confirmed_account)):
    """Получение заявки клиента."""
    return await views.get_application(application_id)


@router.delete(
    "/{application_id}/",
    responses={
        status.HTTP_200_OK: {"description": "Application deleted"},
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

    return {"description": "Application deleted"}


@router.get(
    "/",
    response_model=schemas.ListApplications,
    responses={
        status.HTTP_200_OK: {"description": "Application list"},
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