from fastapi import APIRouter, HTTPException, Depends

from accounts.enums import Permissions
from accounts.schemas import AccountData
from applications.enums import ApplicationStatus
from applications.service import ServiceApplication
from authorization.utils import get_current_user, has_permission
from clients.service import ServiceClient
from drivers.service import ServiceTransport, ServiceDriver
from notifications import schemas, logic, enums, service

router = APIRouter()


@router.post("/transport_offer")
async def create_transport_offer(request: schemas.NotificationBase, account: AccountData = Depends(get_current_user)):
    """Создание уведомления о предложении транспорта по заказу клиента."""
    if not await has_permission(account.id, Permissions.public_api_access):
        raise HTTPException(status_code=400, detail="User is not have permission")

    driver = await ServiceDriver.get_by_account_id(account.id)
    if not driver:
        raise HTTPException(status_code=400, detail="Driver is not found")

    driver_transports = await ServiceTransport.get_driver_transports(driver['id'])
    if len(driver_transports) == 0:
        raise HTTPException(status_code=400, detail="Driver is not have transports")

    transport = await ServiceTransport.get(request.transport_id)
    if not transport:
        raise HTTPException(status_code=400, detail="Transport is not found")

    if transport not in driver_transports:
        raise HTTPException(status_code=400, detail="Driver is not have transport this id")

    application = await ServiceApplication.get(request.application_id)
    if not application:
        raise HTTPException(status_code=400, detail="Application is not found")

    if application['application_status'] != ApplicationStatus.waiting.value:
        raise HTTPException(status_code=400, detail="Application is have ended status")

    notification = await service.ServiceNotifications.get_notifications_by_application_and_transport(
        application_id=application['id'],
        transport_id=transport['id'],
    )
    if notification:
        raise HTTPException(status_code=400, detail="Notification early is created")

    schema = schemas.NotificationCreate(
        notification_type=enums.NotificationTypes.driver.value,
        **request.dict()
    )

    return await logic.create_notification(schema)


@router.post("/application_offer")
async def create_transport_offer(request: schemas.NotificationBase, account: AccountData = Depends(get_current_user)):
    """Создание уведомления о предложении выполнить заказ клиента водител.."""
    if not await has_permission(account.id, Permissions.public_api_access):
        raise HTTPException(status_code=400, detail="User is not have permission")

    transport = await ServiceTransport.get(request.transport_id)
    if not transport:
        raise HTTPException(status_code=400, detail="Transport is not found")

    application = await ServiceApplication.get(request.application_id)
    if not application:
        raise HTTPException(status_code=400, detail="Application is not found")

    client = await ServiceClient.get(account.id)
    if not client:
        raise HTTPException(status_code=400, detail="Client is not found")

    actual_applications = await ServiceApplication.get_actual_applications(client['id'])
    if len(actual_applications) == 0:
        raise HTTPException(status_code=400, detail="Client is not have actual applications")

    if application not in actual_applications:
        raise HTTPException(status_code=400, detail="Client is not have application this id")

    schema = schemas.NotificationCreate(
        notification_type=enums.NotificationTypes.client.value,
        **request.dict()
    )

    return await logic.create_notification(schema)
