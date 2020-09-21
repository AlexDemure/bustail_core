from applications import schemas, service


async def create_application(schema: schemas.ApplicationCreate) -> int:
    """Создание заявки"""
    return await service.ServiceApplication(schema).create()


async def get_actual_applications(client_id: int) -> list:
    """Получение списка актуальных заявок клиента."""
    return await service.ServiceApplication.get_actual_applications(client_id)
