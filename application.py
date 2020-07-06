import uvicorn
from fastapi import FastAPI
from db.database import database
from accounts.models import accounts

app = FastAPI(debug=True)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/account")
async def create_account():
    query = accounts.insert().values()
    account_id = await database.execute(query)
    return account_id


#TODO Сделать для каждого router dependencies=[Depends(get_token_header)]
#
# Он будет выполняться при каждом запросе
# async def get_token_header(x_token: str = Header(...)):
#     if x_token != "fake-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")


# app.include_router(
#     accounts.router,
#     prefix="/account",
#     tags=["Работа с моделью Accounts"],
# )
#
# app.include_router(
#     persons.router,
#     prefix="/person",
#     tags=["Работа с моделью Persons"],
# )
#
# app.include_router(
#     clients.router,
#     prefix="/client",
#     tags=["Работа с моделью Clients"],
# )
#
# app.include_router(
#     applications.router,
#     prefix="/application",
#     tags=["Работа с моделью Applications"],
# )


if __name__ == '__main__':
    uvicorn.run("application:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")