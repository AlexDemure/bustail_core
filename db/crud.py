from sqlalchemy.orm import Session

from core.db import models
from core import schemas


def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()


def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).offset(skip).limit(limit).all()


def create_account(db: Session, account: schemas.AccountCreate):
    db_user = models.Account(login=account.login, password=account.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user