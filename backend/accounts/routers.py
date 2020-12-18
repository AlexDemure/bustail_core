from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from backend.accounts import views, schemas, enums
from backend.accounts.crud import account as account_crud
from backend.auth.utils import response_auth_cookie
from backend.mailing.views import is_verify_code
from backend.common.utils import get_cities
from backend.common.deps import current_account, confirmed_account
from backend.common.responses import auth_responses
from backend.common.schemas import Message


router = APIRouter()


@router.post(
    "/",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Create auth token"},
        status.HTTP_400_BAD_REQUEST: {"description": enums.AccountErrors.phone_already_exist.value},
        status.HTTP_404_NOT_FOUND: {"description": enums.AccountErrors.city_not_found.value}
    }
)
async def create_account(request: schemas.AccountCreate) -> Any:
    """
    Create new user.
    """
    account = await account_crud.find_by_email(email=request.email)
    if account:
        if account.get("verify_at", None):
            raise HTTPException(
                status_code=400,
                detail=enums.AccountErrors.phone_already_exist.value,
            )

    if request.city not in get_cities():
        raise HTTPException(
            status_code=404,
            detail=enums.AccountErrors.city_not_found.value,
        )

    account_id = await views.create_account(request, account)
    return response_auth_cookie(account_id)


@router.get(
    "/me/",
    response_model=schemas.AccountData,
    responses=auth_responses
)
async def read_user_me(account: dict = Depends(confirmed_account)) -> Any:
    """Get current user."""

    return schemas.AccountData(
        id=account['id'],
        fullname=account['fullname'],
        phone=account['phone'],
        email=account['email'],
        city=account['city'],
    )


@router.post(
    "/confirm/",
    response_model=Message,
    responses={
        status.HTTP_200_OK: {"description": "Account confirmed"},
        status.HTTP_400_BAD_REQUEST: {"description": enums.AccountErrors.account_is_confirmed.value},
        status.HTTP_404_NOT_FOUND: {"description": enums.AccountErrors.confirmed_code_is_not_found.value}
    }
)
async def confirmed_account(request: schemas.ConfirmAccount, account: dict = Depends(current_account)) -> Any:
    """
    Create new user.
    """
    if account:
        if account.get("verify_at", None):
            raise HTTPException(
                status_code=400,
                detail=enums.AccountErrors.account_is_confirmed.value,
            )

    if await is_verify_code(account['id'], request.code) is False:
        raise HTTPException(
            status_code=404,
            detail=enums.AccountErrors.confirmed_code_is_not_found.value,
        )

    await views.confirmed_account(account)
    return Message(msg="Account is confirmed")
