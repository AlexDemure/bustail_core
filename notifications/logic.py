from notifications import schemas, service
from drivers.service import ServiceTransport, ServiceDriver
from applications.service import ServiceApplication
from clients.service import ServiceClient


async def create_notification(schema: schemas.NotificationCreate) -> int:
    """Создание уведомления о предложении транспорта по заявке клиента."""
    return await service.ServiceNotifications(schema).create()


async def checking_driver(account_id: int, transport: dict):
    """
    Проверка данных водителя.

    Проверка на наличие карточки водителя.
    Проверка на наличие транспорта.
    Проверка на принадлежность транспорта к его списку.
    """
    driver = await ServiceDriver.get_by_account_id(account_id)
    if not driver:
        raise ValueError("Driver is not found")

    driver_transports = await ServiceTransport.get_driver_transports(driver['id'])
    if len(driver_transports) == 0:
        raise ValueError("Driver is not have transports")

    if transport not in driver_transports:
        raise ValueError("Driver is not have transport this id")


async def checking_client(account_id: int, application: dict):
    """
    Проверка данных клиента.

    Проверка на наличие карточки клиента.
    Проверка на наличие заявок.
    Проверка на принадлежность заявки к его списку.
    """

    client = await ServiceClient.get(account_id)
    if not client:
        raise ValueError("Client is not found")

    actual_applications = await ServiceApplication.get_actual_applications(client['id'])
    if len(actual_applications) == 0:
        raise ValueError("Client is not have actual applications")

    if application not in actual_applications:
        raise ValueError("Client is not have application this id")

