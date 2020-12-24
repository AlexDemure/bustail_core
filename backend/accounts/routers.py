from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from backend.accounts import views, schemas, enums
from backend.accounts.models import Account
from backend.accounts.crud import account as account_crud
from backend.auth.utils import get_token
from backend.auth.schemas import Token
from backend.common.deps import current_account, confirmed_account
from backend.common.enums import BaseMessage
from backend.common.responses import auth_responses
from backend.common.schemas import Message, UpdatedBase
from backend.mailing.views import is_verify_code

router = APIRouter()


@router.post(
    "/",
    response_model=Token,
    responses={
        status.HTTP_201_CREATED: {"description": BaseMessage.obj_is_created.value},
        status.HTTP_400_BAD_REQUEST: {"description": enums.AccountErrors.email_already_exist.value},
        status.HTTP_404_NOT_FOUND: {"description": enums.AccountErrors.city_not_found.value}
    }
)
async def create_account(request: schemas.AccountCreate, response: Response) -> Any:
    """Создание нового пользователя."""
    account = await account_crud.find_by_email(email=request.email)
    if account:
        if account.verified_at is None:
            raise HTTPException(
                status_code=400,
                detail=enums.AccountErrors.email_already_exist.value,
            )

    account_id = await views.create_account(request, account)

    response.status_code = 201
    return Token(access_token=get_token(account_id))


@router.put(
    "/",
    response_model=Message,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_is_changed.value},
        status.HTTP_400_BAD_REQUEST: {"description": enums.AccountErrors.phone_already_exist.value},
        **auth_responses
    }
)
async def update_account(request: schemas.AccountUpdate, account: Account = Depends(confirmed_account)) -> Any:
    """Обновление данных аккаунта."""
    if request.phone:
        other_account = await account_crud.find_by_phone(phone=request.phone)
        if other_account:
            raise HTTPException(
                status_code=400,
                detail=enums.AccountErrors.phone_already_exist.value,
            )

    update_schema = UpdatedBase(
        id=account.id,
        updated_fields=request.dict()
    )
    await account_crud.update(update_schema)
    return Message(msg=BaseMessage.obj_is_changed.value)


@router.get(
    "/me/",
    response_model=schemas.AccountData,
    responses=auth_responses
)
async def read_user_me(account: Account = Depends(confirmed_account)) -> Any:
    """Получение данных текущего пользователя."""

    return schemas.AccountData(
        id=account.id,
        fullname=account.fullname,
        phone=account.phone,
        email=account.email,
        city=account.city,
    )


@router.post(
    "/confirm/",
    response_model=Message,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_is_changed.value},
        status.HTTP_400_BAD_REQUEST: {"description": enums.AccountErrors.account_is_confirmed.value},
        status.HTTP_404_NOT_FOUND: {"description": enums.AccountErrors.confirmed_code_is_not_found.value}
    }
)
async def confirmed_account(request: schemas.ConfirmAccount, account: Account = Depends(current_account)) -> Any:
    """Подтверждение аккаунта через почту."""
    if account:
        if account.verified_at is not None:
            raise HTTPException(
                status_code=400,
                detail=enums.AccountErrors.account_is_confirmed.value,
            )

    if await is_verify_code(account.id, request.code) is False:
        raise HTTPException(
            status_code=404,
            detail=enums.AccountErrors.confirmed_code_is_not_found.value,
        )

    await views.confirmed_account(account)
    return Message(msg=BaseMessage.obj_is_changed.value)


@router.put(
    "/change_password/",
    response_model=Message,
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_is_changed.value},
        status.HTTP_400_BAD_REQUEST: {"description": enums.AccountErrors.url_change_password_is_wrong.value},
        status.HTTP_404_NOT_FOUND: {"description": enums.AccountErrors.confirmed_code_is_not_found.value}
    }
)
async def change_password(request: schemas.ChangePassword, security_token: str) -> Any:
    """Смена пароля."""
    try:
        await views.change_password(request.password, security_token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return Message(msg=BaseMessage.obj_is_changed.value)
