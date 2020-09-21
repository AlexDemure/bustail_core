from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends

from accounts.enums import Permissions
from accounts.schemas import AccountData
from applications import schemas, logic
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

