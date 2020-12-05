import os
import secrets
from typing import Any, Optional
from pydantic import BaseSettings, PostgresDsn, validator
from enum import Enum
from backend.common.enums import Roles, Permissions


class Settings(BaseSettings):
    DOMAIN: str = os.environ.get("DOMAIN")
    API_URL: str = "/api/v1"

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # # 60 minutes * 12 hours = 0.5day

    roles: Enum = Roles
    permissions: Enum = Permissions

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str]) -> Any:
        if isinstance(v, str):
            return v
        # Return URL-connect 'postgresql://postgres:bustail@postgres/bustail'
        return PostgresDsn.build(
            scheme="postgresql",
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            host=os.environ.get("POSTGRES_SERVER"),
            path=f"/{os.environ.get('POSTGRES_DB')}",
        )

    class Config:
        case_sensitive = True


settings = Settings()
