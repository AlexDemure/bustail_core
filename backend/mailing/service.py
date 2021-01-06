import httpx
from structlog import get_logger

from backend.enums.mailing import MailingTypes
from backend.mailing.settings import SERVICE_NAME, BASE_URL
from backend.redis.service import redis

logger = get_logger()


async def service_mailing():
    while True:
        async for task in redis.get_tasks(SERVICE_NAME):
            logger.debug(F"Service:{SERVICE_NAME} accepted task", task=task)

            if task['message_type'] == MailingTypes.send_verify_code.value:
                url = f"{BASE_URL}/message/html/verify_code/"

            elif task['message_type'] == MailingTypes.send_welcome_message.value:
                url = f"{BASE_URL}/message/html/welcome/"

            elif task['message_type'] == MailingTypes.send_change_password_message.value:
                url = f"{BASE_URL}/message/html/change_password/"

            else:
                raise ValueError

            logger.debug(f"Send request in service: {SERVICE_NAME}", url=url)

            async with httpx.AsyncClient() as client:
                response = await client.post(url=url, json=task['data'])

            logger.debug("Accepted response", status_code=response.status_code, text=response.text)

            if response.status_code == 429:
               await redis.append_task_first(SERVICE_NAME, task)
            elif response.status_code != 200:
               raise ValueError
