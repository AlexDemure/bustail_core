from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app.auth import schemas
from app.auth import security
from app.core.config import settings

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_URL}/login/access-token"
)


def get_current_subject(token: str = Depends(reusable_oauth2)) -> int:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    return token_data.sub
