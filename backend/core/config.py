import os
import secrets
from typing import Any, Optional
from pydantic import BaseSettings, PostgresDsn, validator
from enum import Enum
from backend.common.enums import Roles, Permissions


class BaseConfig(BaseSettings):

    class Config:
        case_sensitive = True


class FastApiAuthSettings(BaseConfig):

    DOMAIN: str = os.environ.get("DOMAIN")
    API_URL: str = "/api/v1"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 12  # 60 minutes * 12 hours = 0.5day


class SecuritySettings(BaseConfig):

    SECURITY_TOKEN_EXPIRE_MINUTES = 24 * 60  # 1 day


class MailingMandrillSettings(BaseConfig):

    MAILING_API_KEY: str = os.environ.get("MAILING_API_KEY")
    MAILING_SECRET_KEY: str = os.environ.get("MAILING_SECRET_KEY")
    MAILING_EMAIL: str = os.environ.get("MAILING_EMAIL")
    MAILING_NAME: str = os.environ.get("MAILING_NAME")


class RolesAndPermissionsSettings(BaseConfig):

    roles: Enum = Roles
    permissions: Enum = Permissions


class DBSettings(BaseConfig):

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


applications = [
    FastApiAuthSettings, SecuritySettings, MailingMandrillSettings,
    RolesAndPermissionsSettings, DBSettings
]


class Settings(*applications):

    SECRET_KEY: str = secrets.token_urlsafe(32)


settings = Settings()
