from datetime import timedelta

from fastapi import status
from fastapi_auth import security
from starlette.responses import Response

from backend.core.config import settings


def get_token(account_id: int) -> str:
    return security.create_access_token(
        subject=str(account_id),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def response_auth_cookie(account_id: int) -> Response:
    """Получение респонса с токеном-авторизации"""
    response = security.create_cookie(get_token(account_id))
    response.status_code = status.HTTP_204_NO_CONTENT

    return response
