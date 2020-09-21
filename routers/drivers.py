from fastapi import APIRouter, HTTPException, Depends

from accounts.schemas import AccountData
from accounts.enums import Permissions
from drivers import service, logic, schemas
from authorization.utils import get_current_user, has_permission

router = APIRouter()


@router.post("/")
async def create_driver(account: AccountData = Depends(get_current_user)):
    """Создание водителя."""
    if not await has_permission(account.id, Permissions.public_api_access):
        raise HTTPException(status_code=400, detail="User is not have permission")

    return await logic.create_driver(account.id)


@router.get("/")
async def get_driver(account: AccountData = Depends(get_current_user)):
    """Получение водителя."""
    if not await has_permission(account.id, Permissions.public_api_access):
        raise HTTPException(status_code=400, detail="User is not have permission")

    driver = await service.ServiceDriver.get(account.id)
    if not driver:
        raise HTTPException(status_code=400, detail="Driver is not found")

    return driver


@router.post('/transports')
async def create_transport(request: schemas.TransportBase, account: AccountData = Depends(get_current_user)):
    if not await has_permission(account.id, Permissions.public_api_access):
        raise HTTPException(status_code=400, detail="User is not have permission")

    driver = await service.ServiceDriver.get(account.id)
    if not driver:
        raise HTTPException(status_code=400, detail="Driver is not found")

    schema = schemas.TransportCreate(
        driver_id=driver['id'],
        **request.dict()
    )
    return await logic.create_transport(schema)
