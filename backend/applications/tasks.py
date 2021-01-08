from backend.applications.crud import application as application_crud
from backend.common.schemas import UpdatedBase
from backend.enums.applications import ApplicationStatus


async def completed_applications():
    applications = await application_crud.completed_applications()

    for application in applications:
        updated_schema = UpdatedBase(
            id=application.id,
            updated_fields=dict(application_status=ApplicationStatus.completed)
        )
        await application_crud.update(updated_schema)
