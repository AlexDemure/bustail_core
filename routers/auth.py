from fastapi import APIRouter, HTTPException, status

from accounts.schemas import AuthorizationDataBase
from authorization.schemas import AuthToken
from authorization.utils import create_token, authenticate_user, create_cookie, delete_cookie


router = APIRouter()


@router.post("/login", response_model=AuthToken)
async def login_for_access_token(auth_data: AuthorizationDataBase):
    """Получение авторизационного токена с созданием его в токен."""
    account_id = await authenticate_user(auth_data)
    if not account_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_token(data={"sub": str(account_id)})

    return create_cookie("Authorization", access_token)


@router.get("/logout")
async def logout():
    return delete_cookie("Authorization")



