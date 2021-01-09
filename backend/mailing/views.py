from backend.common.utils import get_current_domain
from backend.enums.mailing import MailingTypes
from backend.mailing import crud
from backend.mailing.settings import SERVICE_NAME
from backend.redis.service import redis
from backend.schemas.mailing import (
    SendVerifyCodeEventCreate, ChangePasswordEventCreate, MailingTask
)
from backend.security.utils import generate_random_code, generate_security_token


async def send_verify_code(account_id: int, email) -> None:
    """Отправка кода подтверждения аккаунта."""
    verify_code = generate_random_code()

    task = MailingTask(
        message_type=MailingTypes.send_verify_code.value,
        data=dict(email=email, message=verify_code)
    )
    await redis.append_task(SERVICE_NAME, task.dict())

    create_schema = SendVerifyCodeEventCreate(
        account_id=account_id,
        message=verify_code
    )
    await crud.send_verify_code_event.create(create_schema)


async def is_verify_code(account_id: int, code: str) -> bool:
    """Проверка наличие подтвержденного кода."""
    code = await crud.send_verify_code_event.find_code(account_id, code)
    return True if code else False


async def send_welcome_message(email: str) -> None:
    """Отправка письма Добро пожаловать."""
    task = MailingTask(
        message_type=MailingTypes.send_welcome_message.value,
        data=dict(email=email)
    )
    await redis.append_task(SERVICE_NAME, task.dict())


async def send_change_password_message(account_id: int, email: str) -> None:
    """Отправка письма со сменой пароля."""
    security_data = dict(account_id=account_id, email=email)
    security_token = generate_security_token(security_data)

    # Ссылка на страницу со сменой пароля.
    confirm_url = f"{get_current_domain()}/change_password/?token={security_token}"

    task = MailingTask(
        message_type=MailingTypes.send_change_password_message.value,
        data=dict(email=email, message=confirm_url)
    )
    await redis.append_task(SERVICE_NAME, task.dict())

    create_schema = ChangePasswordEventCreate(
        email=email,
        message=security_token
    )
    await crud.change_password_event.create(create_schema)


async def is_verify_token(email: str, security_token: str) -> bool:
    """Проверка наличие токена."""
    token = await crud.change_password_event.find_token(email, security_token)
    return True if token else False
