import uvicorn
from fastapi import FastAPI
from db.database import database

from routers import accounts, auth, clients

app = FastAPI(debug=True)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Работа с базовыми токенами авторизации."],
)

app.include_router(
    accounts.router,
    prefix="/account",
    tags=["Работа с моделью Accounts, PersonalData, AuthorizationData"],
)


if __name__ == '__main__':
    uvicorn.run("application:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
