from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.accounts.models import Account
from backend.common.deps import confirmed_account
from backend.common.enums import BaseMessage
from backend.common.responses import auth_responses
from backend.notifications import schemas, views, enums
from backend.drivers.views import is_transport_belongs_driver
from backend.drivers.enums import DriverErrors
from backend.applications.views import get_application
from backend.applications.enums import ApplicationErrors

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.NotificationData,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_already_exist.value},
        status.HTTP_201_CREATED: {"description": BaseMessage.obj_is_created.value},
        status.HTTP_400_BAD_REQUEST: {
            "description": f"{DriverErrors.car_not_belong_to_driver.value} or "
                           f"{ApplicationErrors.application_does_not_belong_this_user.value}"
        },
        **auth_responses
    }
)
async def create_notification(notification_in: schemas.NotificationCreate, account: Account = Depends(confirmed_account)):
    """Создание предложения об услуги."""
    if notification_in.notification_type == enums.NotificationTypes.driver_to_client:
        if await is_transport_belongs_driver(account.id, notification_in.transport_id) is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=DriverErrors.car_not_belong_to_driver.value
            )
    elif notification_in.notification_type == enums.NotificationTypes.client_to_driver:
        application = await get_application(notification_in.application_id)

        if account.id != application.account_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ApplicationErrors.application_does_not_belong_this_user.value
            )

    notification = await views.create_notification(notification_in)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(notification)
    )


@router.put(
    "/",
    response_model=schemas.NotificationData,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_is_changed.value},
        status.HTTP_400_BAD_REQUEST: {
            "description": f"{enums.NotificationErrors.notification_is_have_decision.value} or "
                           f"{ApplicationErrors.application_does_not_belong_this_user.value}"
        },
        status.HTTP_404_NOT_FOUND: {"description": BaseMessage.obj_is_not_found.value},
        **auth_responses
    }
)
async def notification_decision(request: schemas.SetDecision, account: Account = Depends(confirmed_account)):
    """Решение по предложению."""

    notification = await views.get_notification(request.notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BaseMessage.obj_is_not_found.value
        )

    if notification.decision is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=enums.NotificationErrors.notification_is_have_decision.value
        )

    # Если уведомление от водителя тогда смотрим принадлежит ли это заявка данному пользователю.
    if notification.notification_type == enums.NotificationTypes.driver_to_client:
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
    elif notification.notification_type == enums.NotificationTypes.client_to_driver:
        if await is_transport_belongs_driver(account.id, notification.transport_id) is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=DriverErrors.car_not_belong_to_driver.value
            )

    notification = await views.set_decision(notification.id, request.decision)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(notification)
    )
