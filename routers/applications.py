from fastapi import APIRouter, Depends

from db import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.Application)
def create_application(application: schemas.ApplicationCreate):
    application = crud.create_application(application=application)
    return schemas.Application(**application.__dict__, phone=application.client.person.phone)
