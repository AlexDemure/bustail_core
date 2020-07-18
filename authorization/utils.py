from datetime import datetime, timedelta

from starlette.responses import Response
from fastapi import HTTPException, status
from jose import JWTError, jwt
from starlette.requests import Request

from accounts.crud import get_authorization_data
from accounts.schemas import Account, AuthorizationDataBase
from accounts.views import AccountView

from clients.schemas import Client
from clients.views import ClientView

from crypt import verify_password
from .schemas import AuthTokenData, ClientCardTokenData
from .settings import AUTH_SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, TOKEN_DOMAIN


async def authenticate_user(auth: AuthorizationDataBase) -> int:
    """Аутентификация пользователя."""
    auth_data = await get_authorization_data(auth.login)
    if not auth_data:
        return False
    if not verify_password(auth.password, auth_data['password']):
        return False

    return auth_data['account_id']


def create_token(data: dict) -> str:
    """Создание токена."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=12)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, AUTH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_cookie_payload(key: str, request: Request, exception: HTTPException) -> dict:
    cookie = request.cookies.get(key)
    if not cookie:
        raise exception
    else:
        schema, token = cookie.split(" ")

    try:
        payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise exception

    return payload


def create_cookie(key: str, token: str):
    response = Response()

    response.set_cookie(
        key=key,
        value=f"Bearer {token}",
        domain=TOKEN_DOMAIN,
        httponly=True,
        max_age=60 * ACCESS_TOKEN_EXPIRE_MINUTES,
        expires=60 * ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    return response


def delete_cookie(key: str):
    response = Response()

    response.delete_cookie(
        key=key,
        path='/',
        domain=TOKEN_DOMAIN
    )

    return response


async def get_current_user(request: Request) -> Account:
    """Получение текущего пользователя."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Account is not found.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = get_cookie_payload("Authorization", request, credentials_exception)

    account_id = payload.get("sub")
    if account_id is None:
        raise credentials_exception

    token_data = AuthTokenData(account_id=account_id)

    account = await AccountView.get(token_data.account_id)
    if not account:
        raise credentials_exception
    return account


async def get_current_client(request: Request) -> Client:
    """Получение текущего пользователя."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Client card is not found.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = get_cookie_payload("ClientCard", request, credentials_exception)

    client_id = payload.get("sub")
    if client_id is None:
        raise credentials_exception

    token_data = ClientCardTokenData(client_id=client_id)

    client = await ClientView.get("id", token_data.client_id)
    if not client:
        raise credentials_exception
    return client



