import os
import secrets
from typing import Any, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class BaseConfig(BaseSettings):

    class Config:
        case_sensitive = True


class FastApiAuthSettings(BaseConfig):

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 12  # 60 minutes * 12 hours = 0.5day


class SecuritySettings(BaseConfig):

    SECURITY_TOKEN_EXPIRE_MINUTES: int = 60 * 60 * 24  # 1 day


class MailingMandrillSettings(BaseConfig):

    MAILING_SECRET_KEY: str = os.environ.get("MAILING_SECRET_KEY")
    MAILING_EMAIL: str = os.environ.get("MAILING_EMAIL")
    MAILING_NAME: str = os.environ.get("MAILING_NAME")


class DBSettings(BaseConfig):

    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str]) -> Any:
        if isinstance(v, str):
            return v
        # Return URL-connect 'postgresql://postgres:bustail@postgres/bustail'
        return PostgresDsn.build(
            scheme="postgres",
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            host=os.environ.get("POSTGRES_SERVER"),
            path=f"/{os.environ.get('POSTGRES_DB')}",
        )


class TestDBSettings(BaseConfig):

    DATABASE_URI = "sqlite://db.sqlite3"


class YandexObjectStorage(BaseConfig):

    YANDEX_ACCESS_KEY_ID: str = os.environ["YANDEX_ACCESS_KEY_ID"]
    YANDEX_SECRET_ACCESS_KEY: str = os.environ["YANDEX_SECRET_ACCESS_KEY"]
    YANDEX_BUCKET_NAME: str = os.environ["YANDEX_BUCKET_NAME"]

    MAX_FILE_SIZE_MB: int = 100


# DEFAULT SETTINGS
applications = [
    FastApiAuthSettings, SecuritySettings,
    YandexObjectStorage, MailingMandrillSettings,
]


if os.environ.get('ENV', "DEV") == "DEV":
    applications.append(TestDBSettings)
else:
    applications.append(DBSettings)


class Settings(*applications):
    ENV: str = os.environ.get("ENV", "DEV")
    SERVER: str = os.environ.get("SERVER", "http")
    DOMAIN: str = os.environ.get("DOMAIN", "localhost")
    API_URL: str = "/api/v1"

    SECRET_KEY: str = secrets.token_urlsafe(32)


settings = Settings()

