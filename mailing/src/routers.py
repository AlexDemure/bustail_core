from fastapi import APIRouter, HTTPException
from fastapi import status
from fastapi.responses import Response
from structlog import get_logger

from mailing.src import sender
from mailing.src.errors import SendGridError
from mailing.src.responses import responses
from mailing.src.schemas import SendVerifyCodeEvent, BaseEmail, ChangePassword


router = APIRouter()


@router.post(
    "/message/html/verify_code/",
    responses=responses
)
async def send_verify_code(payload: SendVerifyCodeEvent):
    """Отправка кода подтверждения."""
    logger = get_logger().bind(payload=payload.dict())

    try:
        await sender.SendVerifyCodeMessage(payload).send_email()
    except SendGridError as exc:
        logger.error(f"SendGrid API return error {exc.error_type.description}:{exc.error_type.value}")
        raise HTTPException(status_code=exc.error_type.value, detail=exc.error_type.description)

    return Response(content="Message is send", status_code=status.HTTP_200_OK)


@router.post(
    "/message/html/welcome/",
    responses=responses
)
async def send_welcome_message(payload: BaseEmail):
    """Отправка письма добро пожаловать."""
    logger = get_logger().bind(payload=payload.dict())

    try:
        await sender.SendWelcomeMessage(payload).send_email()
    except SendGridError as exc:
        logger.error(f"SendGrid API return error {exc.error_type.description}:{exc.error_type.value}")
        raise HTTPException(status_code=exc.error_type.value, detail=exc.error_type.description)

    return Response(content="Message is send", status_code=status.HTTP_200_OK)


@router.post(
    "/message/html/change_password/",
    responses=responses
)
async def send_change_password_message(payload: ChangePassword):
    """Отправка письма с ссылкой для смены пароля."""
    logger = get_logger().bind(payload=payload.dict())

    try:
        await sender.ChangePasswordMessage(payload).send_email()
    except SendGridError as exc:
        logger.error(f"SendGrid API return error {exc.error_type.description}:{exc.error_type.value}")
        raise HTTPException(status_code=exc.error_type.value, detail=exc.error_type.description)

    return Response(content="Message is send", status_code=status.HTTP_200_OK)
