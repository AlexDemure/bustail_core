from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from backend.object_storage.enums import UploadErrors
from backend.object_storage.utils import check_file_type, check_file_size

from backend.common.deps import confirmed_account
from backend.common.enums import BaseMessage
from backend.common.responses import auth_responses
from backend.common.schemas import Message, UpdatedBase
from backend.drivers.views import (
    get_driver_by_account_id, update_driver, is_transport_belongs_driver, upload_transport_cover,
    create_driver as view_create_driver,
    create_transport as view_create_transport,
    get_transports as view_get_transports,
    get_transport as view_get_transport,
    change_transport_data as view_change_transport_data,
    delete_transport as view_delete_transport,
    get_transport_cover as view_get_transport_cover,
)
from backend.schemas.drivers import (
    DriverBase, DriverCreate, DriverData,
    TransportData, TransportBase, TransportCreate, ListTransports, TransportUpdate,
    TransportPhotoData
)
from backend.enums.drivers import DriverErrors
from backend.accounts.models import Account

router = APIRouter()


@router.post(
    "/",
    response_model=DriverData,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_already_exist.value},
        status.HTTP_201_CREATED: {"description": BaseMessage.obj_is_created.value},
        **auth_responses
    }
)
async def create_driver(request: DriverBase, account: Account = Depends(confirmed_account)):
    """Создание карточки водителя."""
    driver = await get_driver_by_account_id(account.id)
    if driver:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(driver)
        )

    create_schema = DriverCreate(
        account_id=account.id,
        license_number=request.license_number
    )
    driver = await view_create_driver(create_schema, account)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(driver)
    )


@router.put(
    "/",
    response_model=Message,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_is_changed.value},
        status.HTTP_404_NOT_FOUND: {"description": BaseMessage.obj_is_not_found.value},
        **auth_responses
    }
)
async def change_driver_data(request: DriverBase, account: Account = Depends(confirmed_account)):
    """Смена данных в карточки водителя."""
    driver = await get_driver_by_account_id(account.id)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BaseMessage.obj_is_not_found.value
        )

    update_schema = UpdatedBase(id=driver.id, updated_fields=request.dict())
    await update_driver(update_schema)

    return Message(msg=BaseMessage.obj_is_changed.value)


@router.get(
    "/me/",
    response_model=DriverData,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        status.HTTP_404_NOT_FOUND: {"description": BaseMessage.obj_is_not_found.value},
        **auth_responses
    }
)
async def read_driver_me(account: Account = Depends(confirmed_account)):
    """Карточка водителя."""
    driver = await get_driver_by_account_id(account.id)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BaseMessage.obj_is_not_found.value
        )

    return driver


@router.post(
    "/transports/",
    response_model=TransportData,
    responses={
        status.HTTP_201_CREATED: {"description": BaseMessage.obj_is_created.value},
        status.HTTP_400_BAD_REQUEST: {"description": BaseMessage.obj_is_not_created.value},
        status.HTTP_404_NOT_FOUND: {"description": BaseMessage.obj_is_not_found},
        **auth_responses
    }
)
async def create_transport(request: TransportBase, account: Account = Depends(confirmed_account)):
    """Создание карточки транспорта."""
    driver = await get_driver_by_account_id(account.id)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BaseMessage.obj_is_not_found.value
        )

    create_schema = TransportCreate(driver_id=driver.id, **request.dict())
    try:
        transport = await view_create_transport(create_schema)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(transport)
    )


@router.get(
    "/transports/",
    response_model=ListTransports,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        **auth_responses
    }
)
async def get_transports(
        limit: int = 10, offset: int = 0,
        city: str = "", order_by: str = 'price', order_type: str = 'asc'
) -> ListTransports:
    """Получение списка всех заявок."""

    query_params = dict(
        limit=limit, offset=offset, city=city, order_by=order_by, order_type=order_type
    )
    return await view_get_transports(**query_params)


@router.get(
    "/transports/{transport_id}/",
    response_model=TransportData,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        status.HTTP_404_NOT_FOUND: {"description": BaseMessage.obj_is_not_found.value},
        **auth_responses
    }
)
async def get_transport(transport_id: int):
    """Карточка транспорта."""
    transport = await view_get_transport(transport_id)
    if not transport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BaseMessage.obj_is_not_found.value
        )

    return transport


@router.put(
    "/transports/{transport_id}/",
    response_model=Message,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_is_changed.value},
        status.HTTP_400_BAD_REQUEST: {"description": DriverErrors.car_not_belong_to_driver.value},
        status.HTTP_404_NOT_FOUND: {"description": BaseMessage.obj_is_not_found.value},
        **auth_responses
    }
)
async def change_transport_data(
        transport_id: int,
        request: TransportBase,
        account: Account = Depends(confirmed_account)
):
    """Изменение данных в карточке транспорта."""
    driver, transport = await is_transport_belongs_driver(account.id, transport_id)

    transport_up = TransportUpdate(driver_id=driver.id, **request.dict())
    await view_change_transport_data(transport, transport_up)
    return Message(msg=BaseMessage.obj_is_changed.value)


@router.delete(
    "/transports/{transport_id}/",
    response_model=Message,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_is_deleted.value},
        status.HTTP_400_BAD_REQUEST: {"description": DriverErrors.car_not_belong_to_driver.value},
        **auth_responses
    }
)
async def delete_transport(transport_id: int, account: Account = Depends(confirmed_account)):
    """Удаление собственного транспорта."""

    driver, transport = await is_transport_belongs_driver(account.id, transport_id)

    try:
        await view_delete_transport(transport.id)
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return Message(msg=BaseMessage.obj_is_deleted.value)


@router.post(
    "/transports/{transport_id}/covers/",
    response_model=TransportPhotoData,
    responses={
        status.HTTP_201_CREATED: {"description": BaseMessage.obj_is_created.value},
        status.HTTP_400_BAD_REQUEST: {
            "description": f"{UploadErrors.file_is_large.value} or {UploadErrors.mime_type_is_wrong_format.value}"
        },
        status.HTTP_404_NOT_FOUND: {"description": BaseMessage.obj_is_not_found},
        **auth_responses
    }
)
async def create_cover_transport(
        transport_id: int,
        file: UploadFile = File(...),
        account: Account = Depends(confirmed_account)
):
    """Загрузка обложки к транспорту."""

    if check_file_type(file.content_type) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=UploadErrors.mime_type_is_wrong_format.value
        )

    if check_file_size(file.file) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=UploadErrors.file_is_large.value
        )

    driver, transport = await is_transport_belongs_driver(account.id, transport_id)

    cover = await upload_transport_cover(transport, file)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(cover)
    )


@router.get(
    "/transports/{transport_id}/covers/{cover_id}",
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        status.HTTP_400_BAD_REQUEST: {
            "description": f"{UploadErrors.file_is_large.value} or {UploadErrors.mime_type_is_wrong_format.value}"
        },
        status.HTTP_404_NOT_FOUND: {"description": BaseMessage.obj_is_not_found},
        **auth_responses
    }
)
async def get_transport_cover(transport_id: int, cover_id: int):
    """Получение обложки к транспорту."""

    transport = await get_transport(transport_id)
    if not transport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BaseMessage.obj_is_not_found.value
        )

    file_to_bytes, media_type = await view_get_transport_cover(cover_id)

    return Response(content=file_to_bytes, status_code=status.HTTP_200_OK, media_type=media_type)

