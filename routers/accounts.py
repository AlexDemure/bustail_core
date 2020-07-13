from fastapi import APIRouter, HTTPException

from accounts import crud
from accounts.views import AccountView
from accounts.schemas import AccountCreate, Account


router = APIRouter()


@router.post("/", response_model=Account)
async def create_account(account: AccountCreate):
    """Создание пользовательского аккаунта."""
    personal_data = await crud.get_personal_data('phone', account.personal_data.phone)
    if personal_data:
        raise HTTPException(status_code=400, detail="Phone number associated with another account.")

    auth_data = await crud.get_authorization_data(account.authorization_data.login)
    if auth_data:
        raise HTTPException(status_code=400, detail="Login associated with another account.")

    new_account = await AccountView.create(account)
    return new_account


@router.get("/{account_id}", response_model=Account)
async def get_account(account_id: int):
    """Получение аккаунта."""
    account = await AccountView.get(account_id)
    if not account:
        raise HTTPException(status_code=400, detail="Account is not found.")

    return account
