from fastapi import APIRouter, Depends

from db import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.Client)
def create_client(client: schemas.ClientBase):
    person = crud.get_person(phone=client.phone)

    client = schemas.ClientCreate(person_id=person.id)

    return crud.create_client(client=client)


@router.get("/{client_id}", response_model=schemas.Client)
def get_client(client_id: int):
    client = crud.get_client(client_id=client_id)

    return client
