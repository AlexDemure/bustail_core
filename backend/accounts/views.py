from fastapi_auth.security import get_password_hash
from permissions.utils import create_account_role

from backend.accounts.crud import account as account_crud
from backend.accounts.schemas import AccountCreate
from backend.common.enums import BaseSystemErrors, Roles


async def create_account(account_in: AccountCreate):
    assert isinstance(account_in, AccountCreate), BaseSystemErrors.schema_wrong_format.value

    account_in.hashed_password = get_password_hash(account_in.hashed_password)

    account_id = await account_crud.create(account_in)
    await create_account_role(account_id, Roles.customer)

    return account_id
