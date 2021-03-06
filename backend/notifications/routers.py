from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.accounts.models import Account
from backend.applications.views import get_application
from backend.common.deps import confirmed_account
from backend.common.enums import BaseMessage
from backend.common.responses import auth_responses
from backend.common.schemas import Message
from backend.drivers.views import is_transport_belongs_driver
from backend.enums.applications import ApplicationErrors, ApplicationStatus
from backend.enums.drivers import DriverErrors
from backend.enums.notifications import NotificationTypes, NotificationErrors
from backend.notifications.views import create_notification, get_notification, set_decision, delete_notification
from backend.schemas.notifications import NotificationData, NotificationCreate, SetDecision

router = APIRouter()


@router.post(
    "/",
    response_model=NotificationData,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_already_exist.value},
        status.HTTP_201_CREATED: {"description": BaseMessage.obj_is_created.value},
        status.HTTP_400_BAD_REQUEST: {
            "description": f"{DriverErrors.car_not_belong_to_driver.value} or "
                           f"{ApplicationErrors.application_does_not_belong_this_user.value} or"
                           f"{ApplicationErrors.application_has_ended_status.value}"
        },
        **auth_responses
    }
)
async def create_notification_(notification_in: NotificationCreate, account: Account = Depends(confirmed_account)) -> JSONResponse:
    """Создание предложения об услуги."""
    application = await get_application(notification_in.application_id)

    if application.application_status != ApplicationStatus.waiting:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ApplicationErrors.application_has_ended_status.value
        )

    if notification_in.notification_type == NotificationTypes.driver_to_client:
        if await is_transport_belongs_driver(account.id, notification_in.transport_id) is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=DriverErrors.car_not_belong_to_driver.value
            )
    elif notification_in.notification_type == NotificationTypes.client_to_driver:
        if account.id != application.account_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ApplicationErrors.application_does_not_belong_this_user.value
            )

    notification = await create_notification(notification_in)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(notification)
    )


@router.put(
    "/",
    response_model=Message,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_is_changed.value},
        status.HTTP_400_BAD_REQUEST: {
            "description": f"{NotificationErrors.notification_is_have_decision.value} or "
                           f"{ApplicationErrors.application_does_not_belong_this_user.value}"
        },
        status.HTTP_404_NOT_FOUND: {"description": BaseMessage.obj_is_not_found.value},
        **auth_responses
    }
)
async def notification_decision(request: SetDecision, account: Account = Depends(confirmed_account)) -> Message:
    """Решение по предложению."""

    notification = await get_notification(request.notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BaseMessage.obj_is_not_found.value
        )

    if notification.decision is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NotificationErrors.notification_is_have_decision.value
        )

    # Если уведомление от водителя тогда смотрим принадлежит ли это заявка данному пользователю.
    if notification.notification_type == NotificationTypes.driver_to_client:
        application = await get_application(notification.application_id)
        if not application:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=BaseMessage.obj_is_not_found.value
            )

        if application.account_id != account.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ApplicationErrors.application_does_not_belong_this_user.value
            )

    # Если уведомление от клиента тогда смотрим принадлежит ли этот транспорт данному пользователю.
    elif notification.notification_type == NotificationTypes.client_to_driver:
        if await is_transport_belongs_driver(account.id, notification.transport_id) is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=DriverErrors.car_not_belong_to_driver.value
            )

    await set_decision(notification.id, request.decision)

    return Message(msg=BaseMessage.obj_is_changed.value)


@router.delete(
    "/",
    response_model=Message,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_is_deleted.value},
        status.HTTP_400_BAD_REQUEST: {
            "description": f"{NotificationErrors.notification_is_have_decision.value} or "
                           f"{ApplicationErrors.application_does_not_belong_this_user.value}"
        },
        status.HTTP_404_NOT_FOUND: {"description": BaseMessage.obj_is_not_found.value},
        **auth_responses
    }
)
async def notification_decision(request: SetDecision, account: Account = Depends(confirmed_account)) -> Message:
    """Удаление предложения."""
    notification = await get_notification(request.notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BaseMessage.obj_is_not_found.value
        )

    if notification.decision is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NotificationErrors.notification_is_have_decision.value
        )

    # Если уведомление от водителя тогда смотрим принадлежит ли это заявка данному пользователю.
    if notification.notification_type == NotificationTypes.driver_to_client:
        application = await get_application(notification.application_id)
        if not application:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=BaseMessage.obj_is_not_found.value
            )

        if application.account_id != account.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ApplicationErrors.application_does_not_belong_this_user.value
            )

    # Если уведомление от клиента тогда смотрим принадлежит ли этот транспорт данному пользователю.
    elif notification.notification_type == NotificationTypes.client_to_driver:
        if await is_transport_belongs_driver(account.id, notification.transport_id) is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=DriverErrors.car_not_belong_to_driver.value
            )

    await delete_notification(notification.id)

    return Message(msg=BaseMessage.obj_is_deleted.value)

