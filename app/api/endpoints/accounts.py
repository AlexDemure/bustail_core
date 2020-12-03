from typing import Any

from alchemy_permissions.utils import account_role, is_have_permission, create_account_role
from fastapi import APIRouter, Depends, HTTPException
from fastapi_auth.deps import get_current_subject

from app import crud
from app.core.config import Roles, Permissions
from app.core.security import get_password_hash
from app.schemas.account import AccountCreate, AccountData, AccountBase

router = APIRouter()


@router.post("/", response_model=AccountData)
async def create_account(account_in: AccountBase) -> Any:
    """
    Create new user.
    """
    account = await crud.account.find_by_email(email=account_in.email)
    if account:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    schema = AccountCreate(
        full_name=account_in.full_name,
        email=account_in.email,
        hashed_password=get_password_hash(account_in.password)
    )
    account_id = await crud.account.create(schema)

    role_enum = await create_account_role(account_id, Roles.customer)

    account = await crud.account.get(account_id)
    return AccountData(
        full_name=account['full_name'],
        email=account['email'],
        role=role_enum.description
    )


@router.get("/me", response_model=AccountData)
async def read_user_me(current_account_id: int = Depends(get_current_subject),
) -> Any:
    """
    Get current user.
    """
    account = await crud.account.get(current_account_id)
    if not account:
        raise HTTPException(status_code=400, detail="Account is not found")

    role = await account_role(current_account_id)
    if not role:
        raise HTTPException(status_code=400, detail="Role is not found")

    is_permission = await is_have_permission(current_account_id, [Permissions.public_api_access])
    if not is_permission:
        raise HTTPException(status_code=400, detail="Have not permission")

    return AccountData(
        full_name=account['full_name'],
        email=account['email'],
        role=role.description
    )
