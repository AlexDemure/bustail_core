from fastapi import APIRouter, HTTPException, status
from starlette.responses import Response

from authorization.utils import create_access_token, authenticate_user
from authorization.schemas import Token, AuthorizationDataBase
from authorization.settings import ACCESS_TOKEN_EXPIRE_MINUTES, TOKEN_DOMAIN


router = APIRouter()


@router.post("/", response_model=Token)
async def login_for_access_token(auth_data: AuthorizationDataBase):
    account_id = await authenticate_user(auth_data)
    if not account_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": str(account_id)},
    )

    response = Response()

    response.set_cookie(
        "Authorization",
        value=f"Bearer {access_token}",
        domain=TOKEN_DOMAIN,
        httponly=True,
        max_age=60*ACCESS_TOKEN_EXPIRE_MINUTES,
        expires=60*ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    return response

