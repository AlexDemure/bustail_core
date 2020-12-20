from typing import Optional

from fastapi.encoders import jsonable_encoder

from backend.common.enums import BaseSystemErrors
from backend.common.schemas import UpdatedBase
from backend.drivers import schemas
from backend.drivers.crud import driver as driver_crud
from backend.drivers.crud import transport as transport_crud
from backend.drivers.enums import DriverErrors


async def create_driver(driver_in: schemas.DriverCreate, account: dict) -> schemas.DriverData:
    """Создание карточки водителя."""
    assert isinstance(driver_in, schemas.DriverCreate), BaseSystemErrors.schema_wrong_format.value

    driver = await get_driver_by_account_id(account['id'])
    if driver:
        return driver

    driver_id = await driver_crud.create(driver_in)

    driver = await driver_crud.get(driver_id)
    return jsonable_encoder(schemas.DriverData(**driver))


async def get_driver_by_account_id(account_id: int) -> Optional[schemas.DriverData]:
    driver = await driver_crud.find_by_account_id(account_id)
    return jsonable_encoder(schemas.DriverData(**driver)) if driver else None


async def update_driver(driver_up: UpdatedBase) -> None:
    assert isinstance(driver_up, UpdatedBase), BaseSystemErrors.schema_wrong_format.value
    await driver_crud.update(driver_up)


async def create_transport(transport_in: schemas.TransportCreate) -> schemas.TransportData:
    """Создание карточки транспорта."""
    assert isinstance(transport_in, schemas.TransportCreate), BaseSystemErrors.schema_wrong_format.value

    transport = await transport_crud.find_by_params(
        brand=transport_in.brand,
        model=transport_in.model,
        state_number=transport_in.state_number
    )
    if transport:
        raise ValueError(DriverErrors.transport_already_exist.value)

    transport_id = await transport_crud.create(transport_in)
    transport = await get_transport(transport_id)
    assert transport is not None, "Transport is not found"

    return transport


async def get_transport(transport_id: int) -> Optional[schemas.TransportData]:
    transport = await transport_crud.get(transport_id)
    return jsonable_encoder(schemas.TransportData(**transport)) if transport else None


async def change_transport_data(transport: schemas.TransportData, transport_up: schemas.TransportUpdate) -> None:
    """Обновление карточки транспорта."""
    assert isinstance(transport_up, schemas.TransportUpdate), BaseSystemErrors.schema_wrong_format.value

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


async def get_transports(**kwargs) -> schemas.ListTransports:
    """Получение списка всех предложений аренды транспорта."""
    transports = await transport_crud.get_all_transports(**kwargs)
    return schemas.ListTransports(
        transports=[jsonable_encoder(schemas.TransportData(**x)) for x in transports]
    )


async def delete_transport(transport_id: int) -> None:
    await transport_crud.remove(transport_id)

    transport = await transport_crud.get(transport_id)
    assert transport is None, "Transport is not deleted"
