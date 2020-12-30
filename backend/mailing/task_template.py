from uuid import uuid4
from backend.mailing.settings import SERVICE_NAME


def get_task_template(message_type, message_data: dict) -> dict:
    return {
        'message_id': str(uuid4()),
        'service_name': SERVICE_NAME,
        "message_type": message_type,
        'data': message_data
    }
