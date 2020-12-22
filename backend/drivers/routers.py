from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from object_storage.enums import UploadErrors
from object_storage.utils import check_file_type, check_file_size

from backend.common.deps import confirmed_account
from backend.common.enums import BaseMessage
from backend.common.responses import auth_responses
from backend.common.schemas import Message, UpdatedBase
from backend.drivers import schemas, views
from backend.drivers.enums import DriverErrors

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.DriverData,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_already_exist.value},
        status.HTTP_201_CREATED: {"description": BaseMessage.obj_is_created.value},
        **auth_responses
    }
)
async def create_driver(request: schemas.DriverBase, account: dict = Depends(confirmed_account)):
    """Создание карточки водителя."""
    driver = await views.get_driver_by_account_id(account['id'])
    if driver:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(driver)
        )

    create_schema = schemas.DriverCreate(
        account_id=account['id'],
        license_number=request.license_number
    )
    driver = await views.create_driver(create_schema, account)
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
async def change_driver_data(request: schemas.DriverBase, account: dict = Depends(confirmed_account)):
    """Смена данных в карточки водителя."""
    driver = await views.get_driver_by_account_id(account['id'])
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BaseMessage.obj_is_not_found.value
        )

    update_schema = UpdatedBase(id=driver.id, updated_fields=request.dict())
    await views.update_driver(update_schema)

    return Message(msg=BaseMessage.obj_is_changed.value)


@router.get(
    "/me/",
    response_model=schemas.DriverData,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        status.HTTP_404_NOT_FOUND: {"description": BaseMessage.obj_is_not_found.value},
        **auth_responses
    }
)
async def read_driver_me(account: dict = Depends(confirmed_account)):
    """Карточка водителя."""
    driver = await views.get_driver_by_account_id(account['id'])
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BaseMessage.obj_is_not_found.value
        )

    return driver


@router.post(
    "/transports/",
    response_model=schemas.TransportData,
    responses={
        status.HTTP_201_CREATED: {"description": BaseMessage.obj_is_created.value},
        status.HTTP_400_BAD_REQUEST: {"description": BaseMessage.obj_is_not_created.value},
        status.HTTP_404_NOT_FOUND: {"description": BaseMessage.obj_is_not_found},
        **auth_responses
    }
)
async def create_transport(request: schemas.TransportBase, account: dict = Depends(confirmed_account)):
    """Создание карточки транспорта."""
    driver = await views.get_driver_by_account_id(account['id'])
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BaseMessage.obj_is_not_created.value
        )

    create_schema = schemas.TransportCreate(driver_id=driver.id, **request.dict())
    try:
        transport = await views.create_transport(create_schema)
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
    response_model=schemas.ListTransports,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        **auth_responses
    }
)
async def get_transports(
        limit: int = 10, offset: int = 0,
        city: str = "", order_by: str = 'price', order_type: str = 'asc'
) -> schemas.ListTransports:
    """Получение списка всех заявок."""

    query_params = dict(
        limit=limit, offset=offset, city=city, order_by=order_by, order_type=order_type
    )
    return await views.get_transports(**query_params)


@router.get(
    "/transports/{transport_id}/",
    response_model=schemas.TransportData,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        status.HTTP_404_NOT_FOUND: {"description": BaseMessage.obj_is_not_found.value},
        **auth_responses
    }
)
async def get_transport(transport_id: int):
    """Карточка транспорта."""
    transport = await views.get_transport(transport_id)
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
        request: schemas.TransportBase,
        account: dict = Depends(confirmed_account)
):
    """Изменение данных в карточке транспорта."""
    driver, transport = await views.is_transport_belongs_driver(account['id'], transport_id)

    transport_up = schemas.TransportUpdate(driver_id=driver.id, **request.dict())
    await views.change_transport_data(transport, transport_up)
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
async def delete_application(transport_id: int, account: dict = Depends(confirmed_account)):
    """Удаление собственного транспорта."""

    driver, transport = await views.is_transport_belongs_driver(account['id'], transport_id)

    try:
        await views.delete_transport(transport.id)
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return Message(msg=BaseMessage.obj_is_deleted.value)


@router.post(
    "/transports/{transport_id}/covers/",
    response_model=schemas.TransportPhotoData,
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
        account: dict = Depends(confirmed_account)
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

    driver, transport = await views.is_transport_belongs_driver(account['id'], transport_id)

    cover = await views.upload_transport_cover(transport, file)

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
async def get_cover_transport(transport_id: int, cover_id: int):
    """Получение обложки к транспорту."""

    transport = await get_transport(transport_id)
    if not transport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BaseMessage.obj_is_not_found.value
        )

    file_to_bytes, media_type = await views.get_transport_cover(cover_id)

    return Response(content=file_to_bytes, status_code=status.HTTP_200_OK, media_type=media_type)

