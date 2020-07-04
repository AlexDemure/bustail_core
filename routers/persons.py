from fastapi import APIRouter, Depends

from db import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.Person)
async def create_person(person: schemas.PersonBase):
    account = await crud.get_account(account_id=1)

    person = schemas.PersonCreate(
        account_id=account['id'],
        fullname=person.fullname,
        phone=person.phone
    )

    return await crud.create_person(person=person)
