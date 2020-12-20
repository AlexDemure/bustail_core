from security_utils.security import generate_random_code, generate_security_token

from backend.common.utils import get_current_domain
from backend.mailing import schemas, sender, crud


async def send_verify_code(account_id: int, email) -> None:
    """Отправка кода подтверждения аккаунта."""
    verify_code = generate_random_code()

    send_schema = schemas.SendVerifyCodeEvent(email=email, message=verify_code)
    await sender.SendVerifyCodeMessage(send_schema).send_email()

    create_schema = schemas.SendVerifyCodeEventCreate(
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
    send_schema = schemas.BaseEmail(email=email)
    await sender.SendWelcomeMessage(send_schema).send_email()


async def send_change_password_message(account: dict) -> None:
    """Отправка письма со сменой пароля."""
    security_data = dict(account_id=account['id'], email=account['email'])
    security_token = generate_security_token(security_data)

    # Ссылка на страницу со сменой пароля.
    confirm_url = f"{get_current_domain()}/change_password/?token={security_token}"

    send_schema = schemas.ChangePassword(
        message=confirm_url,
        email=account['email']
    )
    await sender.ChangePasswordMessage(send_schema).send_email()

    create_schema = schemas.ChangePasswordEventCreate(
        email=account['email'],
        message=security_token
    )
    await crud.change_password_event.create(create_schema)


async def is_verify_token(email: str, security_token: str) -> bool:
    """Проверка наличие токена."""
    token = await crud.change_password_event.find_token(email, security_token)
    return True if token else False
