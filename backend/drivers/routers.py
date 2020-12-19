from fastapi import APIRouter, Depends, status, HTTPException

from backend.drivers import schemas, enums, views
from backend.common.deps import confirmed_account
from backend.common.responses import auth_responses

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.DriverData,
    responses={
        status.HTTP_201_CREATED: {"description": "Driver is created"},
        **auth_responses
    }
)
async def create_driver(request: schemas.DriverCreate, account: dict = Depends(confirmed_account)) -> schemas.DriverData:
    """Создание карточки водителя."""
    pass
