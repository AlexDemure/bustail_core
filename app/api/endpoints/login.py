from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_auth.deps import get_current_subject
from fastapi_auth.schemas import Token
from fastapi_auth.security import create_access_token

from app import crud
from app.core.config import settings

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user = await crud.account.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="User is not found")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user['id'], expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.get("/login/test-token")
async def test_token(current_user: int = Depends(get_current_subject)):
    """
    Test access token
    """
    user = await crud.account.get(current_user)
    if not user:
        raise HTTPException(status_code=400, detail="User is not found")
    return current_user
