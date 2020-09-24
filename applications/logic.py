from applications import schemas, service, serializer, enums
from notifications.service import ServiceNotifications

async def create_application(schema: schemas.ApplicationCreate) -> int:
    """Создание заявки"""
    return await service.ServiceApplication(schema).create()


async def get_actual_applications(client_id: int) -> list:
    """Получение списка актуальных заявок клиента."""
    return await service.ServiceApplication.get_actual_applications(client_id)


async def get_client_applications(client_id: int) -> schemas.ClientApplications:
    """Получение списка всех заявок клиента c уведомлениями."""
    applications = await service.ServiceApplication.get_client_applications(client_id)

    actual_applications = [x for x in applications if x['application_status'] == enums.ApplicationStatus.waiting.value]

    actual_applications_data = list()
    if len(actual_applications) > 0:
        for application in actual_applications:
            actual_notifications = await ServiceNotifications.get_actual_by_application_id(application['id'])
            actual_applications_data.append(
                serializer.prepare_applications_with_notifications(application, actual_notifications)
            )

    completed_applications = [x for x in applications if x['application_status'] != enums.ApplicationStatus.waiting.value]

    completed_applications_data = list()
    if len(completed_applications) > 0:
        for application in completed_applications:
            completed_applications_data.append(
                serializer.prepare_application(application)
            )

    return schemas.ClientApplications(
        actual_applications=actual_applications_data,
        completed_applications=completed_applications_data
    )
