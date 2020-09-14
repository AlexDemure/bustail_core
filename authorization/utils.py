from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt
from starlette.requests import Request
from starlette.responses import Response

from accounts.schemas import AccountData, AuthorizationDataBase
from accounts.service import (
    AccountService, AuthorizationDataService, AccountRoleService,
    PermissionService, RolePermissionService
)
from accounts.serializer import AccountSerializer
from accounts.enums import Permissions
from crypt import verify_password
from authorization.schemas import AuthTokenData
from authorization.settings import AUTH_SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, TOKEN_DOMAIN


async def authenticate_user(data: AuthorizationDataBase) -> int:
    """Аутентификация пользователя."""
    auth_data = await AuthorizationDataService.get_by_login(data.login)
    if not auth_data:
        return False
    if not verify_password(data.password, auth_data['password']):
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


async def get_current_user(request: Request) -> AccountData:
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

    account = await AccountService.get(token_data.account_id)
    if not account:
        raise credentials_exception

    return AccountSerializer.prepared_data(**account)


async def has_permission(account_id: int, permission: Permissions) -> bool:
    """Проверка на наличие разрешения у пользователя."""
    account_role = await AccountRoleService.get(account_id)
    if not account_role:
        return False

    role_permissions = await RolePermissionService.get_role_permissions(account_role['role_id'])
    for role_permission in role_permissions:
        permission_data = await PermissionService.get(role_permission['permission_id'])
        if permission_data.get('name') == permission.value:
            return True

    return False
