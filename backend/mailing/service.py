from structlog import get_logger

from backend.enums.mailing import MailingTypes
from backend.mailing import sender
from backend.mailing.settings import SERVICE_NAME
from backend.redis.service import redis
from backend.schemas.mailing import SendVerifyCodeEvent, BaseEmail, ChangePassword


logger = get_logger()


async def service_mailing():
    while True:
        async for task in redis.get_tasks(SERVICE_NAME):
            logger.debug(F"Service:{SERVICE_NAME} accepted task", task=task)
            try:
                if task['message_type'] == MailingTypes.send_verify_code.value:
                    schema = SendVerifyCodeEvent(**task['data'])
                    await sender.SendVerifyCodeMessage(schema).send_email()

                elif task['message_type'] == MailingTypes.send_welcome_message.value:
                    schema = BaseEmail(**task['data'])
                    await sender.SendWelcomeMessage(schema).send_email()

                elif task['message_type'] == MailingTypes.send_change_password_message.value:
                    schema = ChangePassword(**task['data'])
                    await sender.ChangePasswordMessage(schema).send_email()

                else:
                    logger.debug(f"Service:{SERVICE_NAME} message_type is not found")
            except:
                await redis.append_task_first(SERVICE_NAME, task)
