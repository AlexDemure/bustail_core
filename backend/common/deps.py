from fastapi_auth.deps import get_subject_from_cookie
from fastapi import Depends, HTTPException
from permissions.utils import is_have_permission
from backend.accounts.crud import account as account_crud
from backend.accounts.enums import AccountErrors
from backend.core.enums import Permissions


async def current_account(current_account_id: int = Depends(get_subject_from_cookie)) -> dict:
    """Получение текущего аккаунта без проверки на подтвержденность."""
    account = await account_crud.get(current_account_id)
    if not account:
        raise HTTPException(status_code=404, detail=AccountErrors.account_not_found.value)

    is_permission = await is_have_permission(current_account_id, [Permissions.public_api_access])
    if not is_permission:
        raise HTTPException(status_code=403, detail=AccountErrors.forbidden)

    return account


async def confirmed_account(current_account_id: int = Depends(get_subject_from_cookie)) -> dict:
    """Получение подтвежденного аккаунта."""
    account = await current_account(current_account_id)

    if account.get("verify_at", None) is None:
        raise HTTPException(status_code=403, detail=AccountErrors.account_not_found)

    return account
