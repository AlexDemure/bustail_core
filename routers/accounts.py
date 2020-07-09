from fastapi import APIRouter, HTTPException

from accounts import crud
from accounts.schemas import (
    AccountBase, Account,
    AuthorizationDataBase, AuthorizationDataCreate,
    PersonalDataBase, PersonalDataCreate,
)


router = APIRouter()


@router.post("/")
async def create_account():
    return await crud.create_account()


@router.get("/{account_id}", response_model=Account)
async def get_account(account_id: int):
    """Получение аккаунта."""
    account_data = await crud.get_account(account_id)
    if not account_data:
        raise HTTPException(status_code=400, detail='Account is not found')
    else:
        data = dict(account_data)

    personal_data = PersonalDataBase(
        fullname=data['fullname'],
        phone=data['phone'],
        email=data.get('email', None),
        birthday=data.get('birthday', None),
        city=data['city']
    )
    authorization_data = AuthorizationDataBase(
        login=data['login'],
        password=data['password']
    )
    return Account(
        id=data['id'],
        registration_date=data['registration_date'],
        authorization_data=authorization_data,
        personal_data=personal_data
    )


@router.post("/{account_id}/authorization_data")
async def create_authorization_data(account_id: int, data: AuthorizationDataBase):
    """Создание авторизационных данных для аккаунта."""
    if await crud.get_authorization_data(account_id):
        raise HTTPException(status_code=400, detail="Account have authorisation data")

    data = AuthorizationDataCreate(account_id=account_id, **data.dict())
    await crud.create_authorization_data(data)


@router.post("/{account_id}/personal_data")
async def create_personal_data(account_id: int, data: PersonalDataBase):
    """Создание персональных данных для аккаунта."""
    if await crud.get_personal_data(account_id):
        raise HTTPException(status_code=400, detail="Account have personal data")

    data = PersonalDataCreate(account_id=account_id, **data.dict())
    await crud.create_personal_data(data)
