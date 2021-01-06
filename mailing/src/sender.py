from uuid import uuid4

import httpx
import jinja2
from structlog import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential

from mailing.src.core.config import settings
from mailing.src.enums import SendGridErrors
from mailing.src.errors import SendGridError
from mailing.src.schemas import BaseEmail, SendVerifyCodeEvent, ChangePassword


class SenderBase:
    loader_path = "mailing/src/templates"  # Откуда брать HTML

    sender_email = settings.MAILING_EMAIL
    sender_name = settings.MAILING_NAME

    validation_schema = BaseEmail  # Используется для проверки схемы.

    template_name = None  # HTML который будет использоваться при отправке
    schema = None
    logger = None
    cid = None

    def __init__(self, schema):
        self.schema = schema
        self.logger = get_logger()
        self.cid = str(uuid4())

    async def send_email(self):
        raise NotImplementedError

    def get_context(self) -> dict:
        raise NotImplementedError

    def prepared_html(self, context: dict) -> str:
        loader = jinja2.FileSystemLoader(self.loader_path)
        env = jinja2.Environment(loader=loader, autoescape=True)
        template = env.get_template(self.template_name)
        return template.render(**context)

    def validate_data(self):
        assert isinstance(self.schema, self.validation_schema), "Schema is wrong format"

    def get_send_grid_template(self, subject: str, html: str) -> dict:
        data = {
            "personalizations": [
                {
                    "to": [
                        {
                            "email": self.schema.email,
                            "name": self.schema.email,
                        }
                    ],
                    "subject": subject,
                }
            ],
            "content": [
                {
                    "type": "text/html",
                    "value": html
                }
            ],
            "from": {
                "email": settings.MAILING_EMAIL,
                "name": settings.MAILING_NAME,
            }
        }

        return data

    @retry(
        wait=wait_exponential(multiplier=1),
        stop=stop_after_attempt(5),
        reraise=True,
    )
    async def send_html(self, subject: str, html: str):

        data = self.get_send_grid_template(subject, html)

        async with httpx.AsyncClient() as client:
            if settings.SEND_MAIL == "yes":
                self.logger.debug("Send request to SendGrid", subject=subject, email=self.schema.email)

                response = await client.post(
                    url='https://api.sendgrid.com/v3/mail/send',
                    headers={"Authorization": f"Bearer {settings.MAILING_SECRET_KEY}"},
                    json=data,
                )
                self.logger.info(f'Confirm response: {response.status_code}')
                if response.status_code != 202:
                    raise SendGridError(SendGridErrors(response.status_code))

            else:
                self.logger.debug("Request is don't send", data=data)


class SendVerifyCodeMessage(SenderBase):
    template_name = 'base.html'

    validation_schema = SendVerifyCodeEvent

    async def send_email(self):
        self.validate_data()

        context = self.get_context()
        html = self.prepared_html(context)
        subject = "Подтвердите регистрацию"

        return await self.send_html(subject, html)

    def get_context(self) -> dict:
        return dict(verify_code=self.schema.message)


class SendWelcomeMessage(SenderBase):
    template_name = 'welcome.html'

    async def send_email(self):
        self.validate_data()

        context = self.get_context()
        html = self.prepared_html(context)
        subject = "Добро пожаловать!"

        return await self.send_html(subject, html)

    def get_context(self) -> dict:
        return dict()


class ChangePasswordMessage(SenderBase):
    template_name = 'change_password.html'

    validation_schema = ChangePassword

    async def send_email(self):
        self.validate_data()

        context = self.get_context()
        html = self.prepared_html(context)
        subject = "Смена пароля"

        return await self.send_html(subject, html)

    def get_context(self) -> dict:
        return dict(url=self.schema.message)
