from fastapi import APIRouter, Depends

from db import crud, schemas
from db.database import SessionLocal, get_db

router = APIRouter()


@router.post("/", response_model=schemas.Client)
def create_client(client: schemas.ClientBase, db: SessionLocal = Depends(get_db)):
    person = crud.get_person(db=db, phone=client.phone)

    client = schemas.ClientCreate(person_id=person.id)

    return crud.create_client(db=db, client=client)


@router.get("/{client_id}", response_model=schemas.Client)
def get_client(client_id: int, db: SessionLocal = Depends(get_db)):
    client = crud.get_client(db=db, client_id=client_id)

    return client
