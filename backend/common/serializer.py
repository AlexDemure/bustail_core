from datetime import datetime


def datetime_to_string(value: datetime) -> str:
    return value.strftime("%d.%m.%y %H:%M")


def string_to_datetime(value: str) -> datetime:
    return datetime.strptime(value, "%d.%m.%y %H:%M")
