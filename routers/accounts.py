from fastapi import APIRouter, HTTPException, Depends

from accounts import crud
from accounts.views import AccountView
from accounts.schemas import (
    AccountCreate, Account,
    PersonalDataBase, PersonalDataUpdate,
    AuthorizationDataBase, AuthorizationDataUpdate,
    ResetPassword, ResetPasswordBase
)

from crypt import get_password_hash, verify_password, get_verify_code

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


@router.post('/reset_password')
async def reset_password(reset_data: ResetPasswordBase):
    """Получение """
    auth_data = await get_authorization_data(reset_data.login)
    if not auth_data:
        raise HTTPException(status_code=400, detail="Login is not found.")

    verify_code = get_verify_code(auth_data['password'])
    return dict(verify_code=verify_code)


@router.put('/reset_password')
async def reset_password(reset_data: ResetPassword):
    """Обновление пароля у аккаунта."""
    auth_data = await get_authorization_data(reset_data.login)
    if not auth_data:
        raise HTTPException(status_code=400, detail="Login is not found.")

    if reset_data.verify_code != get_verify_code(auth_data['password']):
        raise HTTPException(status_code=400, detail="Incorrect verify code.")

    hash_password = get_password_hash(reset_data.password)

    auth_data = AuthorizationDataUpdate(
        account_id=auth_data['account_id'],
        login=reset_data.login,
        password=hash_password,
    )
    await crud.update_auth_data(auth_data)
