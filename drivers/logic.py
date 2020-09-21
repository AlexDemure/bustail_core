from drivers import service, schemas
from accounts.logic import get_account


async def create_driver(account_id: int) -> int:
    """Создание водителя."""
    account = await get_account(account_id)
    if not account:
        raise ValueError("Account is not found")

    driver = await service.ServiceDriver.get(account.id)
    if driver:
        return driver['id']

    return await service.ServiceDriver(schemas.DriverDataCreate(account_id=account.id)).create()

