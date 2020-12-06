from fastapi import APIRouter, Depends, status, HTTPException

from backend.applications import schemas, enums, views
from backend.common.deps import current_account
from backend.common.responses import auth_responses

router = APIRouter()


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


# @router.get("/{client_id}/actual_applications")
# async def get_actual_applications(client_id: int, account: AccountData = Depends(get_current_user)):
#     """Получение актуальных заявок клиента."""
#     if not await has_permission(account.id, Permissions.public_api_access):
#         raise HTTPException(status_code=400, detail="User is not have permission")
#
#     client = await ServiceClient.get(account.id)
#     if not client:
#         raise HTTPException(status_code=400, detail="Client is not found")
#
#     if client['id'] != client_id:
#         raise HTTPException(status_code=400, detail="Access is denied")
#
#     return await logic.get_actual_applications(client['id'])
#
#
# @router.post("/get_all_applications")
# async def get_all_applications(request: schemas.ApplicationFilters, account: AccountData = Depends(get_current_user)):
#     """Получение списка всех заявок для водителей с фильтрами поиска."""
#     if not await has_permission(account.id, Permissions.public_api_access):
#         raise HTTPException(status_code=400, detail="User is not have permission")
#
#     return await service.ServiceApplication(request).get_all_applications()