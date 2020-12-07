from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from backend.accounts import views, schemas, enums
from backend.accounts.crud import account as account_crud
from backend.auth.utils import response_with_token
from backend.common.utils import get_cities
from backend.common.deps import current_account
from backend.common.responses import auth_responses

router = APIRouter()


@router.post(
    "/",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Create auth token"},
        status.HTTP_400_BAD_REQUEST: {"description": enums.AccountErrors.phone_already_exist.value},
        status.HTTP_404_NOT_FOUND: {"description": enums.AccountErrors.city_not_found.value}
    }
)
async def create_account(account_in: schemas.AccountCreate) -> Any:
    """
    Create new user.
    """
    account = await account_crud.find_by_phone(phone=account_in.phone)
    if account:
        raise HTTPException(
            status_code=400,
            detail=enums.AccountErrors.phone_already_exist.value,
        )

    if account_in.city not in get_cities():
        raise HTTPException(
            status_code=404,
            detail=enums.AccountErrors.city_not_found.value,
        )

    account_id = await views.create_account(account_in)
    return response_with_token(account_id)


@router.get(
    "/me/",
    response_model=schemas.AccountData,
    responses=auth_responses
)
async def read_user_me(account: dict = Depends(current_account)) -> Any:
    """Get current user."""

    return schemas.AccountData(
        id=account['id'],
        fullname=account['fullname'],
        phone=account['phone'],
        city=account['city'],
    )
