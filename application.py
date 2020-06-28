import uvicorn
from fastapi import FastAPI, Depends

from db import crud, models, schemas
from db.database import SessionLocal, engine

app = FastAPI(debug=True)


models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


# @app.post("/account/", response_model=schemas.Account)
# def create_user(account: schemas.AccountCreate, db: SessionLocal = Depends(get_db)):
#     return crud.create_account(db=db, account=account)


if __name__ == '__main__':
    uvicorn.run("application:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")