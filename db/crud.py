from sqlalchemy.orm import Session

from db import models, schemas


def get_account(db: Session, login: str):
    return db.query(models.Account).filter(models.Account.login == login).first()


def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).offset(skip).limit(limit).all()


def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(login=account.login, password=account.password)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def get_person(db: Session, phone: str):
    return db.query(models.Person).filter(models.Person.phone == phone).first()


def get_persons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Person).offset(skip).limit(limit).all()


def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(
        account_id=person.account_id,
        fullname=person.fullname,
        phone=person.phone
    )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(person_id=client.person_id)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def create_application(db: Session, application: schemas.ApplicationCreate):
    db_application = models.Application(
        client_id=application.client_id,
        to_go_from=application.to_go_from,
        to_go_when=application.to_go_when,
        count_seats=application.count_seats,
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

