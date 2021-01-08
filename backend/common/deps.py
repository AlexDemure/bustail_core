from fastapi import Depends, HTTPException

from backend.accounts.crud import account as account_crud
from backend.accounts.models import Account
from backend.auth.deps import get_subject_from_token
from backend.enums.accounts import AccountErrors
from backend.permissions.enums import Permissions
from backend.permissions.utils import is_have_permission


async def current_account(current_account_id: int = Depends(get_subject_from_token)) -> Account:
    """Получение текущего аккаунта без проверки на подтвержденность."""
    account = await account_crud.get(current_account_id)
    if not account:
        raise HTTPException(status_code=404, detail=AccountErrors.account_not_found.value)

    is_permission = await is_have_permission(current_account_id, [Permissions.public_api_access])
    if not is_permission:
        raise HTTPException(status_code=403, detail=AccountErrors.forbidden.value)

    return account


async def confirmed_account(current_account_id: int = Depends(get_subject_from_token)) -> Account:
    """Получение подтвежденного аккаунта."""
    account = await current_account(current_account_id)

    if account.verified_at is None:
        raise HTTPException(status_code=404, detail=AccountErrors.account_not_found.value)

    return account
