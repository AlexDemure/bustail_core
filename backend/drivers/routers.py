from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse

from backend.drivers import schemas, enums, views
from backend.common.deps import confirmed_account
from backend.common.responses import auth_responses
from backend.common.schemas import Message, UpdatedBase

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.DriverData,
    responses={
        status.HTTP_200_OK: {"description": "Driver already exist"},
        status.HTTP_201_CREATED: {"description": "Driver is created"},
        **auth_responses
    }
)
async def create_driver(request: schemas.DriverBase, account: dict = Depends(confirmed_account)):
    """Создание карточки водителя."""
    driver = await views.get_driver_by_account_id(account['id'])
    if driver:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=driver.dict()
        )

    create_schema = schemas.DriverCreate(
        account_id=account['id'],
        license_number=request.license_number
    )
    driver = await views.create_driver(create_schema, account)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=driver.dict()
    )


@router.put(
    "/",
    response_model=Message,
    responses={
        status.HTTP_200_OK: {"description": "Data is changed"},
        status.HTTP_404_NOT_FOUND: {"description": "Driver is not found"},
        **auth_responses
    }
)
async def change_driver_data(request: schemas.DriverBase, account: dict = Depends(confirmed_account)):
    """Смена данных в карточки водителя."""
    driver = await views.get_driver_by_account_id(account['id'])
    if not driver:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver is not found"
        )

    update_schema = UpdatedBase(id=driver.id, updated_fields=request.dict())
    await views.update_driver(update_schema)

    return Message(msg="Data is changed")


@router.get(
    "/me/",
    response_model=schemas.DriverData,
    responses={
        status.HTTP_200_OK: {"description": "Driver data"},
        status.HTTP_404_NOT_FOUND: {"description": "Driver is not found"},
        **auth_responses
    }
)
async def read_driver_me(account: dict = Depends(confirmed_account)):
    """Карточка водителя."""
    driver = await views.get_driver_by_account_id(account['id'])
    if not driver:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver is not found"
        )

    return driver
