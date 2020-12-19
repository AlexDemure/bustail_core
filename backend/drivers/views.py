from backend.drivers.schemas import DriverCreate, DriverData
from backend.drivers.crud import driver as driver_crud
from backend.common.schemas import UpdatedBase
from backend.common.enums import BaseSystemErrors
from typing import Optional


async def create_driver(driver_in: DriverCreate, account: dict) -> DriverData:
    """Создание карточки водителя."""
    assert isinstance(driver_in, DriverCreate), BaseSystemErrors.schema_wrong_format.value

    driver = await get_driver_by_account_id(account['id'])
    if driver:
        return driver

    driver_id = await driver_crud.create(driver_in)

    driver = await driver_crud.get(driver_id)
    return DriverData(**driver)


async def get_driver_by_account_id(account_id: int) -> Optional[DriverData]:
    driver = await driver_crud.find_by_account_id(account_id)
    return DriverData(**driver) if driver else None


async def update_driver(driver_up: UpdatedBase) -> None:
    assert isinstance(driver_up, UpdatedBase), BaseSystemErrors.schema_wrong_format.value
    await driver_crud.update(driver_up)
