import os
import secrets
from typing import Any, Optional
from pydantic import BaseSettings, PostgresDsn, validator
from enum import Enum


class Roles(Enum):
    """
    Типы пользователей в системе
    """
    customer = "Customer"
    admin = "Admin"

    @property
    def description(self):
        if self is self.customer:
            return "Customer"
        elif self is self.admin:
            return "Admin"

    def get_permissions(self):
        if self is self.customer:
            return [x for x in Permissions if x != Permissions.admin_api_access]
        elif self is self.admin:
            return [x for x in Permissions if x != Permissions.public_api_access]


class Permissions(Enum):
    """
    Доступы ограничений в системе
    """
    public_api_access = "public_api_access"
    admin_api_access = "admin_api_access"

    @property
    def description(self):
        if self is self.public_api_access:
            return "Access to all api methods on the client side."
        elif self is self.admin_api_access:
            return "Access to all api methods for the administrator."


class Settings(BaseSettings):

    API_URL: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # # 60 minutes * 24 hours * 8 days = 8 days

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

    roles = Roles
    permissions = Permissions

    class Config:
        case_sensitive = True


settings = Settings()
