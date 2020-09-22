from fastapi import APIRouter, HTTPException, Depends

from accounts.enums import Permissions
from accounts.schemas import AccountData
from applications.enums import ApplicationStatus
from applications.service import ServiceApplication
from authorization.utils import get_current_user, has_permission
from drivers.service import ServiceTransport
from notifications import schemas, logic, enums, service
from common.schemas import UpdateBase

router = APIRouter()


@router.post("/transport_offer")
async def create_transport_offer(request: schemas.NotificationBase, account: AccountData = Depends(get_current_user)):
    """Создание уведомления о предложении транспорта по заказу клиента."""
    if not await has_permission(account.id, Permissions.public_api_access):
        raise HTTPException(status_code=400, detail="User is not have permission")

    transport = await ServiceTransport.get(request.transport_id)
    if not transport:
        raise HTTPException(status_code=400, detail="Transport is not found")

    try:
        await logic.checking_driver(account.id, transport)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{str(e)}")

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

    try:
        await logic.checking_client(account.id, application)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{str(e)}")

    schema = schemas.NotificationCreate(
        notification_type=enums.NotificationTypes.client.value,
        **request.dict()
    )

    return await logic.create_notification(schema)


@router.post('/decision')
async def notification_decision(request: schemas.NotificationDecision, account: AccountData = Depends(get_current_user)):
    """Решение по уведомелению."""
    if not await has_permission(account.id, Permissions.public_api_access):
        raise HTTPException(status_code=400, detail="User is not have permission")

    notification = await service.ServiceNotifications.get(request.id)
    if not notification:
        raise HTTPException(status_code=400, detail="Notification is not found")

    if notification['decision'] is not None:
        raise HTTPException(status_code=400, detail="Notification is have ended decision")

    transport = await ServiceTransport.get(request.transport_id)
    if not transport:
        raise HTTPException(status_code=400, detail="Transport is not found")

    application = await ServiceApplication.get(request.application_id)
    if not application:
        raise HTTPException(status_code=400, detail="Application is not found")

    if request.notification_type == enums.NotificationTypes.driver.value:
        try:
            await logic.checking_driver(account.id, transport)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"{str(e)}")

    elif request.notification_type == enums.NotificationTypes.client.value:
        try:
            await logic.checking_client(account.id, application)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"{str(e)}")

    else:
        raise HTTPException(status_code=400, detail="Notification type is wrong format")

    #TODO доделать проставку в application driver_id и confirmed_at
    data = UpdateBase(id=notification['id'], updated_fields=dict(decision=request.decision))
    return await service.ServiceNotifications(data).update()
