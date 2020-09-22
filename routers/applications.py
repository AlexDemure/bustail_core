from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends

from accounts.enums import Permissions
from accounts.schemas import AccountData
from applications import schemas, logic, service
from authorization.utils import get_current_user, has_permission
from clients.service import ServiceClient

router = APIRouter()


@router.post("/")
async def create_application(request: schemas.ApplicationBase, account: AccountData = Depends(get_current_user)):
    """Создание заявки."""
    if not await has_permission(account.id, Permissions.public_api_access):
        raise HTTPException(status_code=400, detail="User is not have permission")

    client = await ServiceClient.get(account.id)
    if not client:
        raise HTTPException(status_code=400, detail="Client is not found")

    schema = schemas.ApplicationCreate(
        client_id=client['id'],
        expired_at=request.to_go_when + timedelta(days=7),
        **request.dict()
    )
    return await logic.create_application(schema)


@router.get("/{client_id}/actual_applications")
async def get_actual_applications(client_id: int, account: AccountData = Depends(get_current_user)):
    """Получение актуальных заявок клиента."""
    if not await has_permission(account.id, Permissions.public_api_access):
        raise HTTPException(status_code=400, detail="User is not have permission")

    client = await ServiceClient.get(account.id)
    if not client:
        raise HTTPException(status_code=400, detail="Client is not found")

    if client['id'] != client_id:
        raise HTTPException(status_code=400, detail="Access is denied")

    return await logic.get_actual_applications(client['id'])


@router.post("/get_all_applications")
async def get_all_applications(request: schemas.ApplicationFilters, account: AccountData = Depends(get_current_user)):
    """Получение списка всех заявок для водителей с фильтрами поиска."""
    if not await has_permission(account.id, Permissions.public_api_access):
        raise HTTPException(status_code=400, detail="User is not have permission")

    return await service.ServiceApplication(request).get_all_applications()
