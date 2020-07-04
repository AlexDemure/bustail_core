from fastapi import APIRouter

from db import crud, schemas

router = APIRouter()


# @router.post("/", response_model=schemas.Account)
# def create_user(account: schemas.AccountCreate):
#     return crud.create_account(account=account)

@router.get("/{account_id}", response_model=schemas.Account)
async def get_account(account_id: int):
    return await crud.get_account(account_id=account_id)


@router.post("/", response_model=schemas.Account)
async def create_account(account: schemas.AccountCreate):
    return await crud.create_account(account=account)
