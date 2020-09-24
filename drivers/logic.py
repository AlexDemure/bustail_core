from drivers import service, schemas
from accounts.logic import get_account
from drivers.serializer import prepare_transport_with_notifications
from drivers.schemas import TransportWithNotifications
from notifications.service import ServiceNotifications


async def create_driver(account_id: int) -> int:
    """Создание водителя."""
    account = await get_account(account_id)
    if not account:
        raise ValueError("Account is not found")

    driver = await service.ServiceDriver.get_by_account_id(account.id)
    if driver:
        return driver['id']

    return await service.ServiceDriver(schemas.DriverDataCreate(account_id=account.id)).create()


async def create_transport(schema: schemas.TransportCreate) -> int:
    """Создание транспорта"""
    return await service.ServiceTransport(schema).create()


async def get_transports(driver_id: int) -> schemas.TransportsWithNotifications:
    """Получение списках всех транспортов водителя."""
    transports = await service.ServiceTransport.get_driver_transports(driver_id)

    data = list()
    if len(transports) > 0:
        for transport in transports:
            notifications = await ServiceNotifications.get_actual_by_transport_id(transport['id'])
            data.append(prepare_transport_with_notifications(transport, notifications))

    return schemas.TransportsWithNotifications(transports=data)
