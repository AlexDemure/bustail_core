from datetime import datetime

from backend.auth.security import get_password_hash
from backend.permissions.utils import create_account_role
from backend.security.utils import verify_security_token

from backend.accounts.crud import account as account_crud
from backend.accounts.enums import AccountErrors
from backend.accounts.models import Account
from backend.accounts.schemas import AccountCreate
from backend.common.enums import BaseSystemErrors
from backend.common.schemas import UpdatedBase
from backend.permissions.enums import Roles
from backend.mailing.views import send_verify_code, send_welcome_message, is_verify_token


async def create_account(account_in: AccountCreate, account: Account = None) -> int:
    """
    Создание аккаунта клиента.

    Также в методе создается роль к аккаунту и отправка письма с кодом подтверждения.
    """
    assert isinstance(account_in, AccountCreate), BaseSystemErrors.schema_wrong_format.value

    account_in.hashed_password = get_password_hash(account_in.hashed_password)

    # Если аккаунт уже есть в системе но не подтвержден - делаем отправку письма занова.
    if account:
        account_id = account.id

        # Если пароль изменился заменяем на более новый
        if account.hashed_password != account_in.hashed_password:
            updated_schema = UpdatedBase(
                id=account.id,
                updated_fields=dict(hashed_password=account_in.hashed_password)
            )
            await account_crud.update(updated_schema)

    else:
        account = await account_crud.create(account_in)
        await create_account_role(account.id, Roles.customer)

    await send_verify_code(account.id, account_in.email)

    return account.id


async def confirmed_account(account: Account) -> None:
    """Подтверждение аккаунта."""
    updated_schema = UpdatedBase(
        id=account.id,
        updated_fields=dict(verified_at=datetime.utcnow())
    )
    await account_crud.update(updated_schema)

    await send_welcome_message(account.email)


async def change_password(password: str, security_token: str) -> None:
    """Изменение пароля через токен подтверждения."""

    context = verify_security_token(security_token)  # Получение данных токена.
    if context is None:
        raise ValueError(AccountErrors.url_change_password_is_wrong.value)

    if await is_verify_token(context.email, security_token) is False:  # Чтение события о смене пароля.
        raise ValueError(AccountErrors.url_change_password_is_wrong.value)

    account = await account_crud.get(object_id=context['account_id'])
    if not account:
        raise ValueError(AccountErrors.account_not_found.value)

    update_schema = UpdatedBase(
        id=account.id,
        updated_fields=dict(hashed_password=get_password_hash(password))
    )
    await account_crud.update(update_schema)
