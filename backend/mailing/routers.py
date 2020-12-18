from fastapi import APIRouter, HTTPException, status

from fastapi import APIRouter, HTTPException, status

from backend.mailing.schemas import BaseEmail
from backend.mailing.views import send_change_password_message
from backend.common.schemas import Message
from backend.accounts.enums import AccountErrors
from backend.accounts.crud import account as account_crud

router = APIRouter()


@router.post(
    '/change_password/',
    response_model=Message,
    responses={
        status.HTTP_200_OK: {'description': 'Email is sent'},
        status.HTTP_404_NOT_FOUND: {"description": AccountErrors.account_not_found.value}
    }
)
async def change_password(request: BaseEmail):
    """Отправка email-ссылки на изменение пароля аккаунта."""
    account = await account_crud.find_by_email(email=request.email)
    if not account:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=AccountErrors.account_not_found.value)

    await send_change_password_message(account)

    return Message(msg='Email is sent')
