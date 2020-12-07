from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional

from backend.applications import schemas, enums, views
from backend.common.deps import current_account
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
async def get_account_applications(account: dict = Depends(current_account)) -> schemas.ListApplications:
    """
    Получение списка заявок клиента.

    Не относится к заявкам водителя.
    """
    return await views.get_account_applications(account)


@router.post(
    "/",
    response_model=schemas.ApplicationData,
    responses={
        status.HTTP_201_CREATED: {"description": "Application is created"},
        status.HTTP_400_BAD_REQUEST: {"description": enums.ApplicationErrors.to_go_when_wrong_format.value},
        **auth_responses
    }
)
async def create_application(application_in: schemas.ApplicationBase, account: dict = Depends(current_account)):
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
async def get_application(application_id: int, account: dict = Depends(current_account)):
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
async def delete_application(application_id: int, account: dict = Depends(current_account)):
    """Получение заявки клиента."""
    try:
        await views.delete_application(account, application_id)
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"description": "Application deleted"}


# @router.post("/get_all_applications")
# async def get_all_applications(request: schemas.ApplicationFilters, account: AccountData = Depends(get_current_user)):
#     """Получение списка всех заявок для водителей с фильтрами поиска."""
#     if not await has_permission(account.id, Permissions.public_api_access):
#         raise HTTPException(status_code=400, detail="User is not have permission")
#
#     return await service.ServiceApplication(request).get_all_applications()