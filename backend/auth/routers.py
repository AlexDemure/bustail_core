from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.accounts.crud import account as account_crud
from backend.accounts.enums import AccountErrors
from backend.auth.utils import get_token
from backend.auth.schemas import Token
from backend.common.enums import BaseMessage

router = APIRouter()


@router.post(
    "/login/access-token/",
    response_model=Token,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        status.HTTP_404_NOT_FOUND: {"description": BaseMessage.obj_is_not_found.value}
    }
)
async def login_access_cookie(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    account = await account_crud.authenticate(form_data.username, form_data.password)
    if not account:
        raise HTTPException(status_code=404, detail=AccountErrors.account_not_found.value)

    if account.get("verify_at", None) is None:
        raise HTTPException(status_code=404, detail=AccountErrors.account_not_found.value)

    return Token(access_token=get_token(account['id']))

