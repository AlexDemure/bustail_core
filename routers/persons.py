from fastapi import APIRouter, Depends

from db import crud, schemas
from db.database import SessionLocal, get_db

router = APIRouter()


@router.post("/", response_model=schemas.Person)
def create_person(person: schemas.PersonBase, db: SessionLocal = Depends(get_db)):
    account = crud.get_account(db=db, login=person.phone)

    person = schemas.PersonCreate(
        account_id=account.id,
        fullname=person.fullname,
        phone=person.phone
    )

    return crud.create_person(db=db, person=person)