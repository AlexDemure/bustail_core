from fastapi import APIRouter, HTTPException, Depends

from accounts.schemas import AccountData
from accounts.enums import Permissions
from clients import service, logic
from applications.logic import get_client_applications
from applications.schemas import ClientApplications
from authorization.utils import get_current_user, has_permission

router = APIRouter()


@router.post("/")
async def create_client(account: AccountData = Depends(get_current_user)):
    """Создание клиента."""
    if not await has_permission(account.id, Permissions.public_api_access):
        raise HTTPException(status_code=400, detail="User is not have permission")

    return await logic.create_client(account.id)


@router.get("/")
async def get_client(account: AccountData = Depends(get_current_user)):
    """Получение клиента."""
    if not await has_permission(account.id, Permissions.public_api_access):
        raise HTTPException(status_code=400, detail="User is not have permission")

    client = await service.ServiceClient.get(account.id)
    if not client:
        raise HTTPException(status_code=400, detail="Client is not found")

    return client


@router.get('/get_applications', response_model=ClientApplications)
async def get_applications(account: AccountData = Depends(get_current_user)):
    """Получение списка заявок клиента."""
    if not await has_permission(account.id, Permissions.public_api_access):
        raise HTTPException(status_code=400, detail="User is not have permission")

    client = await service.ServiceClient.get(account.id)
    if not client:
        raise HTTPException(status_code=400, detail="Client is not found")

    return await get_client_applications(client['id'])
