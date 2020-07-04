from .database import database
from db import models, schemas



async def get_account(account_id: int) -> schemas.Account:
    account = dict(await database.fetch_one(models.accounts.select().where(models.accounts.c.id == account_id)))
    return schemas.Account(**account)


async def create_account(account: schemas.AccountCreate) -> schemas.Account:
    account_id = models.accounts.insert().values(**account.dict())
    return schemas.Account(**account.dict(), account_id=account_id)

# def get_accounts(skip: int = 0, limit: int = 100):
#     return db.query(models.Account).offset(skip).limit(limit).all()
#
#
# def create_account(account: schemas.AccountCreate):
#     db_account = models.Account(login=account.login, password=account.password)
#     db.add(db_account)
#     db.commit()
#     db.refresh(db_account)
#     return db_account
#
#
# def get_person(phone: str):
#     return db.query(models.Person).filter(models.Person.phone == phone).first()
#
#
# def get_persons(skip: int = 0, limit: int = 100):
#     return db.query(models.Person).offset(skip).limit(limit).all()
#
#
# def get_client(client_id: int):
#     return db.query(models.Client).filter(models.Client.id == client_id).first()
#
#
async def create_person(person: schemas.PersonCreate):
    db_person = models.persons.insert().values(**person.dict())
    person_id = await database.execute(db_person)
    return schemas.Person(**person.dict(), id=person_id)

    # db_person = models.Person(
    #     account_id=person.account_id,
    #     fullname=person.fullname,
    #     phone=person.phone
    # )
    # db.add(db_person)
    # db.commit()
    # db.refresh(db_person)
    # return db_person

#
# def create_client(client: schemas.ClientCreate):
#     db_client = models.Client(person_id=client.person_id)
#     db.add(db_client)
#     db.commit()
#     db.refresh(db_client)
#     return db_client
#
#
# def create_application(application: schemas.ApplicationCreate):
#     db_application = models.Application(
#         client_id=application.client_id,
#         to_go_from=application.to_go_from,
#         to_go_when=application.to_go_when,
#         count_seats=application.count_seats,
#     )
#     db.add(db_application)
#     db.commit()
#     db.refresh(db_application)
#     return db_application
#
