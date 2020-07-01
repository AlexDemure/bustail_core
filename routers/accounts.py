from fastapi import APIRouter, Depends

from db import crud, schemas
from db.database import SessionLocal, get_db

router = APIRouter()


@router.post("/", response_model=schemas.Account)
def create_user(account: schemas.AccountCreate, db: SessionLocal = Depends(get_db)):
    return crud.create_account(db=db, account=account)
