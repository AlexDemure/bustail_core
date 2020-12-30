from structlog import get_logger

from backend.enums.mailing import MailingTypes
from backend.mailing import sender
from backend.mailing.settings import SERVICE_NAME
from backend.redis.service import redis
from backend.schemas.mailing import SendVerifyCodeEvent
import aioredis
import asyncio
import uvicorn

from fastapi import FastAPI, Request

from backend.redis import ques

logger = get_logger()


# async def service_mailing():
#     while True:
#         async for task in redis.get_tasks(SERVICE_NAME):
#             logger.debug(F"Service:{SERVICE_NAME} accepted task", task=task)
#             try:
#                 if task['message_type'] == MailingTypes.send_verify_code.value:
#                     schema = SendVerifyCodeEvent(**task['data'])
#                     await sender.SendVerifyCodeMessage(schema).send_email()
#                 else:
#                     logger.debug(f"Service:{SERVICE_NAME} message_type is not found")
#             except:
#                 await redis.append_task_first(SERVICE_NAME, task)


async def service_mailing(redis_pool: aioredis.commands.Redis):
    while True:
        async for data_in in ques.get_tasks(redis_pool, 'tasks'):
            try:
                print(data_in['message'])
            except:
                await ques.append_task_first(
                    redis_pool, 'tasks', data_in
                )
            finally:
                await asyncio.sleep(1)

        await asyncio.sleep(10)
