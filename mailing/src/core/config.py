import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    SEND_MAIL: str = os.environ.get("SEND_MAIL", "no").lower()

    MAILING_SECRET_KEY: str = os.environ.get("MAILING_SECRET_KEY")
    MAILING_EMAIL: str = os.environ.get("MAILING_EMAIL")
    MAILING_NAME: str = os.environ.get("MAILING_NAME")
    API_URL: str = "/api/v1/mailing"

    class Config:
        case_sensitive = True


settings = Settings()

