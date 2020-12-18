from fastapi_auth.security import get_password_hash
from permissions.utils import create_account_role
from datetime import datetime

from backend.accounts.crud import account as account_crud
from backend.accounts.schemas import AccountCreate
from backend.common.enums import BaseSystemErrors, Roles
from backend.common.schemas import UpdatedBase
from backend.mailing.views import send_verify_code, send_welcome_message


async def create_account(account_in: AccountCreate, account: dict = None) -> int:
    """
    Создание аккаунта клиента.

    Также в методе создается роль к аккаунту и отправка письма с кодом подтверждения.
    """
    assert isinstance(account_in, AccountCreate), BaseSystemErrors.schema_wrong_format.value

    account_in.hashed_password = get_password_hash(account_in.hashed_password)

    # Если аккаунт уже есть в системе но не подтвержден - делаем отправку письма занова.
    if account:
        account_id = account['id']

        # Если пароль изменился заменяем на более новый
        if account['hashed_password'] != account_in.hashed_password:
            updated_schema = UpdatedBase(
                id=account['id'],
                updated_fields=dict(hashed_password=account_in.hashed_password)
            )
            await account_crud.update(updated_schema)

    else:
        account_id = await account_crud.create(account_in)
        await create_account_role(account_id, Roles.customer)

    await send_verify_code(account_id, account_in.email)

    return account_id


async def confirmed_account(account: dict) -> None:
    """Подтверждение аккаунта."""
    updated_schema = UpdatedBase(
        id=account['id'],
        updated_fields=dict(verify_at=datetime.utcnow())
    )
    await account_crud.update(updated_schema)

    await send_welcome_message(account['email'])
