from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


from auth.schemas import Token
from auth.security import create_access_token
from auth.deps import get_current_subject
router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    print(form_data.password, form_data.username)
    return {
        "access_token": create_access_token(1),
        "token_type": "bearer",
    }

@router.get("/login/test-token")
def test_token(current_user: int = Depends(get_current_subject)):
    """
    Test access token
    """
    return current_user
