from typing import Optional
from security_utils.security import generate_random_code, generate_security_token, verify_security_token

from backend.mailing import schemas, sender, crud


async def send_verify_code(account_id: int, email) -> None:
    """Отправка кода подтверждения аккаунта."""
    verify_code = generate_random_code()

    send_schema = schemas.SendVerifyCodeEvent(email=email, verify_code=verify_code)
    await sender.SendVerifyCodeMessage(send_schema).send_email()

    create_schema = schemas.SendVerifyCodeEventCreate(
        account_id=account_id,
        verify_code=verify_code
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
    params = dict(account_id=account['id'], email=account['email'])

    send_schema = schemas.ChanePassword(
        security_token=generate_security_token(**params),
        email=account['email']
    )
    await sender.ChangePasswordMessage(send_schema).send_email()