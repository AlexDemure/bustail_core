from typing import Optional, Tuple, List
from uuid import uuid4

from fastapi import HTTPException, status
from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from backend.object_storage.enums import FileStorages, FileMimetypes
from backend.object_storage.uploader import ObjectStorage
from backend.object_storage.utils import get_file_hash

from backend.common.enums import BaseMessage
from backend.common.enums import BaseSystemErrors
from backend.common.schemas import UpdatedBase
from backend.core.config import settings
from backend.schemas.drivers import (
    DriverCreate, DriverData, TransportData, TransportCreate,
    ListTransports, TransportUpdate, TransportPhotoData, TransportPhotoCreate
)
from backend.drivers.crud import (
    driver as driver_crud,
    transport as transport_crud,
    transport_covers as transport_covers_crud
)
from backend.drivers.serializer import prepare_transports_with_notifications, prepare_transport_with_photos
from backend.enums.drivers import DriverErrors
from backend.accounts.models import Account


object_storage = ObjectStorage(
    settings.YANDEX_ACCESS_KEY_ID, settings.YANDEX_SECRET_ACCESS_KEY, settings.YANDEX_BUCKET_NAME
)


async def create_driver(driver_in: DriverCreate, account: Account) -> DriverData:
    """Создание карточки водителя."""
    assert isinstance(driver_in, DriverCreate), BaseSystemErrors.schema_wrong_format.value

    driver = await get_driver_by_account_id(account.id)
    if driver:
        return driver

    driver = await driver_crud.create(driver_in)
    return DriverData(**driver.__dict__)


async def get_driver_by_account_id(account_id: int) -> Optional[DriverData]:
    driver = await driver_crud.find_by_account_id(account_id)
    return DriverData(**driver.__dict__) if driver else None


async def update_driver(driver_up: UpdatedBase) -> None:
    assert isinstance(driver_up, UpdatedBase), BaseSystemErrors.schema_wrong_format.value
    await driver_crud.update(driver_up)


async def create_transport(transport_in: TransportCreate) -> TransportData:
    """Создание карточки транспорта."""
    assert isinstance(transport_in, TransportCreate), BaseSystemErrors.schema_wrong_format.value

    transport = await transport_crud.find_by_params(
        brand=transport_in.brand,
        model=transport_in.model,
        state_number=transport_in.state_number
    )
    if transport:
        raise ValueError(DriverErrors.transport_already_exist.value)

    transport = await transport_crud.create(transport_in)
    return TransportData(**transport.__dict__)


async def get_transport(transport_id: int) -> Optional[TransportData]:
    transport = await transport_crud.get(transport_id)
    return TransportData(**transport.__dict__) if transport else None


async def change_transport_data(transport: TransportData, transport_up: TransportUpdate) -> None:
    """Обновление карточки транспорта."""
    assert isinstance(transport_up, TransportUpdate), BaseSystemErrors.schema_wrong_format.value

    transport_data = await transport_crud.find_by_params(
        brand=transport_up.brand,
        model=transport_up.model,
        state_number=transport_up.state_number
    )
    if transport_data:
        raise ValueError(DriverErrors.transport_already_exist.value)

    update_schema = UpdatedBase(
        id=transport.id,
        updated_fields=transport_up.dict()
    )
    await transport_crud.update(update_schema)


async def get_transports(**kwargs) -> ListTransports:
    """Получение списка всех предложений аренды транспорта."""
    transports = await transport_crud.get_all_transports(**kwargs)
    return ListTransports(
        transports=[prepare_transport_with_photos(x, x.transport_covers.related_objects) for x in transports]
    )


async def delete_transport(transport_id: int) -> None:
    await transport_crud.remove(transport_id)

    transport = await transport_crud.get(transport_id)
    assert transport is None, "Transport is not deleted"


async def upload_transport_cover(transport: TransportData, file: UploadFile) -> TransportPhotoData:
    """Загрузка обложки к транспорту через бакет."""

    file_hash = get_file_hash(file.file)  # Получение хеша файла с передачей SpooledTempFile.

    # Попытка найти файл в БД по хешу и айди транспорта
    file_object = await transport_covers_crud.find_transport_by_hash(transport.id, file_hash)
    if file_object:
        return TransportPhotoData(**file_object)

    file_media_type = FileMimetypes(file.content_type)

    # Путь где файл будет храниться covers/uuid.file_format
    file_uri = f"{FileStorages.covers.path}{str(uuid4())}{file_media_type.file_format}"

    # Загрузка файла в облако.
    if settings.ENV == "PROD":
        object_storage.upload(
            file=file.file,
            content_type=file.content_type,
            file_url=file_uri
        )

    transport_cover_in = TransportPhotoCreate(
        transport_id=transport.id,
        file_uri=file_uri,
        file_hash=file_hash,
        media_type=file_media_type
    )

    transport_cover = await transport_covers_crud.create(transport_cover_in)
    return TransportPhotoData(**transport_cover.__dict__)


async def get_transport_cover(transport_cover_id: int) -> Tuple[bytes, str]:
    """Получение облокжи транспорта со скачиванием обложки из бакета."""
    transport_cover = await transport_covers_crud.get(transport_cover_id)

    file_content = object_storage.download(transport_cover['file_uri'])

    return file_content, transport_cover['media_type'].value


async def is_transport_belongs_driver(account_id: int, transport_id: int) -> tuple:
    """Проверка принадлежности водителя к транспорту."""

    driver = await get_driver_by_account_id(account_id)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BaseMessage.obj_is_not_created.value
        )

    transport = await get_transport(transport_id)
    if not transport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BaseMessage.obj_is_not_found.value
        )

    # Если транспорт не принадлежит данному водителю.
    if transport.driver_id != driver.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=DriverErrors.car_not_belong_to_driver.value
        )

    return driver, transport


async def get_driver(driver_id: int) -> Optional[DriverData]:
    driver = await driver_crud.get(driver_id)
    return DriverData(**driver.__dict__) if driver else None


async def get_driver_by_transport_id(transport_id: int) -> Optional[DriverData]:
    transport = await transport_crud.get(transport_id)
    if not transport:
        raise ValueError(BaseMessage.obj_is_not_found.value)

    driver = await get_driver(transport.driver_id)
    if not driver:
        raise ValueError(BaseMessage.obj_is_not_found.value)

    return driver


async def get_transport_with_notifications(driver: DriverData) -> List[TransportData]:
    transports = await transport_crud.get_transports_with_notifications(driver.id)
    return [prepare_transports_with_notifications(x, x.notifications) for x in transports]
