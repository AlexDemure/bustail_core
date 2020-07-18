from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import Response

from accounts import crud
from accounts.views import AccountView
from accounts.schemas import (
    AccountCreate, Account,
    PersonalDataBase, PersonalDataUpdate,
    AuthorizationDataBase, AuthorizationDataUpdate
)

from crypt import get_password_hash, verify_password

from authorization.utils import get_current_user, get_authorization_data, delete_auth_cookie


router = APIRouter()


@router.post("/", response_model=Account)
async def create_account(account: AccountCreate):
    """Создание пользовательского аккаунта."""
    personal_data = await crud.get_personal_data('phone', account.personal_data.phone)
    if personal_data:
        raise HTTPException(status_code=400, detail="Phone number associated with another account.")

    auth_data = await get_authorization_data(account.authorization_data.login)
    if auth_data:
        raise HTTPException(status_code=400, detail="Login associated with another account.")

    new_account = await AccountView.create(account)
    return new_account


@router.get("/", response_model=Account)
async def get_account(account: Account = Depends(get_current_user)):
    """Получение аккаунта."""
    account = await AccountView.get(account.id)
    if not account:
        raise HTTPException(status_code=400, detail="Account is not found.")

    return account


@router.delete("/")
async def delete_account(account: Account = Depends(get_current_user)):
    await crud.delete_account(account.id)
    return delete_auth_cookie()


@router.put('/personal_data', response_model=Account)
async def update_person_data(update_data: PersonalDataBase, account: Account = Depends(get_current_user)):
    personal_data = await crud.get_personal_data('phone', update_data.phone, account.id)
    if personal_data:
        raise HTTPException(status_code=400, detail="Phone number associated with another account.")

    update_data = PersonalDataUpdate(account_id=account.id, **update_data.dict())
    await crud.update_personal_data(update_data)

    return await AccountView.get(account.id)


@router.put('/authorization_data', response_model=Account)
async def update_auth_data(update_data: AuthorizationDataBase, account: Account = Depends(get_current_user)):
    auth_data = await get_authorization_data(update_data.login, account.id)
    if auth_data:
        raise HTTPException(status_code=400, detail="Login associated with another account.")

    if verify_password(update_data.password, account.authorization_data.password):
        update_data.password = account.authorization_data.password
    else:
        update_data.password = get_password_hash(update_data.password)

    update_data = AuthorizationDataUpdate(account_id=account.id, **update_data.dict())
    await crud.update_auth_data(update_data)

    return await AccountView.get(account.id)
