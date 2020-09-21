from applications import schemas, service


async def create_application(schema: schemas.ApplicationCreate) -> int:
    """Создание заявки"""
    return await service.ServiceApplication(schema).create()

