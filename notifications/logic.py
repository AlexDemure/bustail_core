from notifications import schemas, service


async def create_notification(schema: schemas.NotificationCreate) -> int:
    """Создание уведомления о предложении транспорта по заявке клиента."""
    return await service.ServiceNotifications(schema).create()
