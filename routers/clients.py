from fastapi import APIRouter, Depends, HTTPException, status

from accounts.schemas import Account
from authorization.utils import (
    get_current_user, create_cookie, delete_cookie,
    create_token, get_current_client
)
from authorization.schemas import ClientCardToken

from clients import crud
from clients.schemas import ClientCreate, Client
from clients.views import ClientView


router = APIRouter()


@router.post("/")
async def create_client(account: Account = Depends(get_current_user)):
    """Создание карточки клиента."""
    client_data = await ClientView.get('account_id', account.id)
    if client_data:
        raise HTTPException(status_code=400, detail="Account have client card.")

    client_data = ClientCreate(account_id=account.id)

    client_id = await ClientView.create(client_data)

    client_token = create_token(data={"sub": str(client_id)})

    return create_cookie("ClientCard", client_token)


@router.get("/", response_model=Client)
async def get_client(client: Client = Depends(get_current_client)):
    """Получение карточки клиента."""
    client_data = await ClientView.get('id', client.id)
    if not client_data:
        raise HTTPException(status_code=400, detail="Client card is not found.")

    return client_data


@router.delete("/")
async def delete_client(client: Client = Depends(get_current_client)):
    """Получение карточки клиента."""
    await ClientView.delete(client.id)
    delete_cookie("ClientCard")


@router.get('/login')
async def login(account: Account = Depends(get_current_user)):
    """Авторизация в качестве клиента."""
    client = await ClientView.get("account_id", account.id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Client is not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    client_token = create_token(data={"sub": str(client.id)})

    return create_cookie("ClientCard", client_token)


@router.get("/logout")
async def logout():
    return delete_cookie("ClientCard")
