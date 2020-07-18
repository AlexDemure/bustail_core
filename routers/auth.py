from fastapi import APIRouter, HTTPException, status

from accounts.schemas import AuthorizationDataBase
from authorization.schemas import Token
from authorization.utils import create_access_token, authenticate_user, create_auth_cookie, delete_auth_cookie


router = APIRouter()


@router.post("/login", response_model=Token)
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

    return create_auth_cookie(access_token)


@router.post("/logout")
async def logout():
    return delete_auth_cookie()



