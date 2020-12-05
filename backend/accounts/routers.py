from datetime import timedelta
from typing import Any

from permissions.utils import account_role, is_have_permission, create_account_role
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_auth.deps import get_subject_from_cookie
from fastapi_auth.security import create_access_token, create_cookie, get_password_hash

from backend.core.config import settings
from backend.accounts.schemas import AccountCreate, AccountData, AccountBase
from backend.common.enums import Roles, Permissions

from backend.accounts.crud import account as account_crud

router = APIRouter()


@router.post(
    "/",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Create auth token"},
        status.HTTP_400_BAD_REQUEST: {"description": "The user with this username already exists in the system."}
    }
)
async def create_account(account_in: AccountBase) -> Any:
    """
    Create new user.
    """
    account = await account_crud.find_by_email(email=account_in.email)
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
    account_id = await account_crud.create(schema)
    await create_account_role(account_id, Roles.customer)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(account_id, expires_delta=access_token_expires)
    return create_cookie(token)


@router.get(
    "/me",
    response_model=AccountData,
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden."},
        status.HTTP_404_NOT_FOUND: {"description": "Account not found or Role not found"}
    }
)
async def read_user_me(current_account_id: int = Depends(get_subject_from_cookie)) -> Any:
    """
    Get current user.
    """
    account = await account_crud.get(current_account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account is not found")

    role = await account_role(current_account_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role is not found")

    is_permission = await is_have_permission(current_account_id, [Permissions.public_api_access])
    if not is_permission:
        raise HTTPException(status_code=403, detail="Forbidden")

    return AccountData(
        full_name=account['full_name'],
        email=account['email'],
        role=role.description
    )
