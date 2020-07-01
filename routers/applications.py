from fastapi import APIRouter, Depends

from db import crud, schemas
from db.database import SessionLocal, get_db

router = APIRouter()


@router.post("/", response_model=schemas.Application)
def create_application(application: schemas.ApplicationCreate, db: SessionLocal = Depends(get_db)):
    application = crud.create_application(db=db, application=application)
    return schemas.Application(**application.__dict__, phone=application.client.person.phone)
